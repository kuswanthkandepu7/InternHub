import os
from urllib.parse import urlparse, unquote
from functools import wraps
from uuid import uuid4
from werkzeug.utils import secure_filename

import mysql.connector
from dotenv import load_dotenv
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, flash, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

# Resume uploads: PDF, DOC, DOCX only; maximum file size is 5 MB.
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads", "resumes")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}


def allowed_resume(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_RESUME_EXTENSIONS


def db():
    uri = os.environ.get("DATABASE_URL")
    if not uri:
        raise RuntimeError("DATABASE_URL is missing. Add your Aiven URI to .env.")
    parsed = urlparse(uri)
    if parsed.scheme not in ("mysql", "mysql+mysqlconnector"):
        raise RuntimeError("DATABASE_URL must start with mysql://")
    config = {
        "host": parsed.hostname, "port": parsed.port or 3306,
        "user": unquote(parsed.username or ""), "password": unquote(parsed.password or ""),
        "database": parsed.path.lstrip("/").split("?")[0],
        "connection_timeout": 15, "autocommit": False, "ssl_disabled": False,
    }
    ca_file = os.environ.get("MYSQL_SSL_CA")
    if ca_file:
        config.update(ssl_ca=ca_file, ssl_verify_cert=True, ssl_verify_identity=True)
    return MySQLSession(config)


class MySQLSession:
    def __init__(self, config):
        self.config, self.connection, self.cursor = config, None, None

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor(dictionary=True)
        return self

    def execute(self, query, params=()):
        self.cursor.execute(query.replace("?", "%s"), params)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.connection and self.connection.is_connected():
                self.connection.rollback() if exc_type else self.connection.commit()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
        return False


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "error")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


def role_required(role):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if session.get("role") != role:
                flash("You do not have permission to access that page.", "error")
                return redirect(url_for("index"))
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def get_companies():
    with db() as con:
        return con.execute(
            """SELECT company_id, company_name, industry, description, website,
                      email, phone, location, logo_url, created_at
               FROM companies ORDER BY company_name"""
        ).fetchall()


def resolve_company_name(form):
    company_id = form.get("company_id", "").strip()
    if company_id:
        with db() as con:
            row = con.execute(
                "SELECT company_name FROM companies WHERE company_id=?", (company_id,)
            ).fetchone()
        if not row:
            raise ValueError("Please select a valid company.")
        return row["company_name"]
    # Supports the original internship form, which has a text input named company.
    return form.get("company", "").strip()


@app.route("/")
def index():
    q = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    mode = request.args.get("mode", "").strip()
    company_filter = request.args.get("company", "").strip()
    sql = """SELECT i.*, u.name AS recruiter_name
             FROM internships i JOIN users u ON u.id=i.recruiter_id WHERE 1=1"""
    params = []
    if q:
        sql += " AND (i.title LIKE ? OR i.company LIKE ? OR i.category LIKE ?)"
        params.extend([f"%{q}%"] * 3)
    if location:
        sql += " AND i.location LIKE ?"
        params.append(f"%{location}%")
    if mode:
        sql += " AND i.mode=?"
        params.append(mode)
    if company_filter:
        sql += " AND i.company=?"
        params.append(company_filter)
    sql += " ORDER BY i.featured DESC, i.created_at DESC"
    with db() as con:
        internships = con.execute(sql, tuple(params)).fetchall()
        companies = con.execute(
            "SELECT company_id, company_name FROM companies ORDER BY company_name"
        ).fetchall()
    return render_template("index.html", internships=internships, q=q,
                           location=location, mode=mode, companies=companies,
                           company=company_filter)


# COMPANY DIRECTORY AND REGISTRATION

@app.route("/companies")
def companies():
    rows = get_companies()
    return render_template_string("""
    <!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Companies | InternHub</title><style>
    body{font-family:Arial,sans-serif;max-width:1000px;margin:35px auto;padding:0 18px;background:#f7f8fc;color:#202532}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
    .card{background:white;border:1px solid #e3e7ef;border-radius:12px;padding:20px}
    a{color:#3157c8;text-decoration:none}.btn{display:inline-block;background:#3157c8;color:white;padding:10px 14px;border-radius:8px}
    .muted{color:#687086}</style></head><body>
    <p><a href="{{ url_for('index') }}">← Home</a>
    {% if session.get('role') == 'recruiter' %} · <a class="btn" href="{{ url_for('new_company') }}">Add company</a>{% endif %}</p>
    <h1>Companies</h1>
    {% if rows %}<div class="grid">{% for c in rows %}<article class="card">
      {% if c.logo_url %}<img src="{{ c.logo_url }}" alt="" style="max-width:100px;max-height:60px">{% endif %}
      <h2>{{ c.company_name }}</h2><p class="muted">{{ c.industry or 'Industry not specified' }}</p>
      <p>{{ c.description or '' }}</p><p>{{ c.location or '' }}</p>
      {% if c.website %}<a href="{{ c.website }}" target="_blank" rel="noopener">Website</a>{% endif %}
    </article>{% endfor %}</div>{% else %}<p>No companies added yet.</p>{% endif %}
    </body></html>""", rows=rows)


@app.route("/company/new", methods=["GET", "POST"])
@role_required("recruiter")
def new_company():
    if request.method == "POST":
        name = request.form.get("company_name", "").strip()
        values = [
            name, request.form.get("industry", "").strip(),
            request.form.get("description", "").strip(),
            request.form.get("website", "").strip(),
            request.form.get("email", "").strip(),
            request.form.get("phone", "").strip(),
            request.form.get("location", "").strip(),
            request.form.get("logo_url", "").strip()
        ]
        if not name:
            flash("Company name is required.", "error")
        else:
            try:
                with db() as con:
                    duplicate = con.execute(
                        "SELECT company_id FROM companies WHERE LOWER(company_name)=LOWER(?)",
                        (name,)
                    ).fetchone()
                    if duplicate:
                        flash("This company is already registered.", "error")
                    else:
                        con.execute(
                            """INSERT INTO companies
                            (company_name,industry,description,website,email,phone,location,logo_url)
                            VALUES(?,?,?,?,?,?,?,?)""",
                            tuple(v or None for v in values)
                        )
                        flash("Company added successfully.", "success")
                        return redirect(url_for("companies"))
            except mysql.connector.Error:
                app.logger.exception("Company insert failed")
                flash("Could not add company. Verify that the companies table exists and matches the SQL schema.", "error")

    return render_template_string("""
    <!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Add company | InternHub</title><style>
    body{font-family:Arial,sans-serif;max-width:680px;margin:35px auto;padding:0 18px;background:#f7f8fc}
    form{background:white;padding:24px;border:1px solid #e3e7ef;border-radius:12px}
    label{display:block;margin-top:13px;font-weight:bold}input,textarea{box-sizing:border-box;width:100%;padding:10px;margin-top:5px;border:1px solid #ccd2df;border-radius:7px}
    button{margin-top:18px;padding:11px 17px;background:#3157c8;color:white;border:0;border-radius:8px}
    a{color:#3157c8;text-decoration:none}</style></head><body>
    <p><a href="{{ url_for('companies') }}">← Companies</a></p><h1>Add a company</h1>
    {% with messages=get_flashed_messages(with_categories=true) %}{% for category,message in messages %}<p>{{ message }}</p>{% endfor %}{% endwith %}
    <form method="post">
      <label>Company name *</label><input name="company_name" required maxlength="150">
      <label>Industry</label><input name="industry" maxlength="100">
      <label>Description</label><textarea name="description" rows="4"></textarea>
      <label>Website</label><input name="website" type="url">
      <label>Contact email</label><input name="email" type="email">
      <label>Phone</label><input name="phone">
      <label>Location</label><input name="location">
      <label>Logo URL</label><input name="logo_url" type="url">
      <button type="submit">Save company</button>
    </form></body></html>""")


# AUTHENTICATION

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")
        if not name or not email or len(password) < 6 or role not in ("student", "recruiter"):
            flash("Enter valid details. Password must contain at least 6 characters.", "error")
            return redirect(url_for("register"))
        try:
            with db() as con:
                con.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                            (name, email, generate_password_hash(password), role))
            flash("Account created. Please log in.", "success")
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:
            flash("That email is already registered.", "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        with db() as con:
            user = con.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session.clear()
            session.update(user_id=user["id"], name=user["name"], role=user["role"])
            return redirect(url_for("dashboard"))
        flash("Incorrect email or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


# DASHBOARDS

@app.route("/dashboard")
@login_required
def dashboard():
    if session["role"] == "student":
        with db() as con:
            applications = con.execute(
                """SELECT a.*, i.title, i.company, i.location
                   FROM applications a JOIN internships i ON i.id=a.internship_id
                   WHERE a.student_id=? ORDER BY a.created_at DESC""",
                (session["user_id"],)
            ).fetchall()
        return render_template("student_dashboard.html", applications=applications)
    with db() as con:
        listings = con.execute(
            """SELECT i.*,
               (SELECT COUNT(*) FROM applications a WHERE a.internship_id=i.id) AS applicant_count
               FROM internships i WHERE recruiter_id=? ORDER BY created_at DESC""",
            (session["user_id"],)
        ).fetchall()
    return render_template("recruiter_dashboard.html", listings=listings)


# INTERNSHIPS

@app.route("/internship/new", methods=["GET", "POST"])
@role_required("recruiter")
def new_internship():
    company_rows = get_companies()
    if request.method == "POST":
        try:
            company = resolve_company_name(request.form)
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("new_internship"))
        fields = [
            request.form.get("title", "").strip(), company,
            request.form.get("location", "").strip(), request.form.get("mode", "").strip(),
            request.form.get("category", "").strip(), request.form.get("stipend", "").strip(),
            request.form.get("description", "").strip()
        ]
        if not all(fields[i] for i in (0, 1, 2, 3, 4, 6)):
            flash("Please complete all required fields and select a company.", "error")
        else:
            with db() as con:
                con.execute(
                    """INSERT INTO internships
                    (recruiter_id,title,company,location,mode,category,stipend,description)
                    VALUES(?,?,?,?,?,?,?,?)""",
                    (session["user_id"], *fields)
                )
            flash("Internship published successfully.", "success")
            return redirect(url_for("dashboard"))
    return render_template("internship_form.html", internship=None, companies=company_rows)


@app.route("/internship/<int:internship_id>")
def internship_detail(internship_id):
    with db() as con:
        item = con.execute(
            """SELECT i.*, u.name AS recruiter_name FROM internships i
               JOIN users u ON u.id=i.recruiter_id WHERE i.id=?""",
            (internship_id,)
        ).fetchone()
        applied = False
        if item and session.get("role") == "student":
            applied = con.execute(
                "SELECT id FROM applications WHERE internship_id=? AND student_id=?",
                (internship_id, session["user_id"])
            ).fetchone() is not None
    if not item:
        flash("Internship not found.", "error")
        return redirect(url_for("index"))
    return render_template("detail.html", item=item, applied=applied)


@app.route("/internship/<int:internship_id>/apply", methods=["POST"])
@role_required("student")
def apply(internship_id):
    message = request.form.get("message", "").strip()
    resume = request.files.get("resume")

    if not resume or not resume.filename:
        flash("Please upload your resume before applying.", "error")
        return redirect(url_for("internship_detail", internship_id=internship_id))

    original_name = secure_filename(resume.filename)
    if not original_name or not allowed_resume(original_name):
        flash("Resume must be a PDF, DOC, or DOCX file.", "error")
        return redirect(url_for("internship_detail", internship_id=internship_id))

    extension = original_name.rsplit(".", 1)[1].lower()
    stored_name = f"{uuid4().hex}.{extension}"
    saved_path = os.path.join(UPLOAD_FOLDER, stored_name)

    try:
        with db() as con:
            exists = con.execute(
                "SELECT id FROM internships WHERE id=?", (internship_id,)
            ).fetchone()
            if not exists:
                flash("Internship not found.", "error")
                return redirect(url_for("index"))

            already_applied = con.execute(
                "SELECT id FROM applications WHERE internship_id=? AND student_id=?",
                (internship_id, session["user_id"])
            ).fetchone()
            if already_applied:
                flash("You have already applied for this internship.", "error")
                return redirect(url_for("internship_detail", internship_id=internship_id))

            resume.save(saved_path)
            try:
                con.execute(
                    """INSERT INTO applications
                       (internship_id, student_id, message, resume_filename)
                       VALUES (?, ?, ?, ?)""",
                    (internship_id, session["user_id"], message, stored_name)
                )
            except Exception:
                if os.path.exists(saved_path):
                    os.remove(saved_path)
                raise

        flash("Application and resume submitted successfully.", "success")
    except mysql.connector.IntegrityError:
        if os.path.exists(saved_path):
            os.remove(saved_path)
        flash("You have already applied for this internship.", "error")
    except mysql.connector.Error:
        if os.path.exists(saved_path):
            os.remove(saved_path)
        app.logger.exception("Application submission failed")
        flash("Could not submit your application. Please check the database and try again.", "error")

    return redirect(url_for("internship_detail", internship_id=internship_id))


@app.route("/application/<int:application_id>/resume")
@role_required("recruiter")
def download_resume(application_id):
    # Recruiters may download resumes only for applications to their own internships.
    with db() as con:
        application = con.execute(
            """SELECT a.resume_filename
               FROM applications a
               JOIN internships i ON i.id = a.internship_id
               WHERE a.id=? AND i.recruiter_id=?""",
            (application_id, session["user_id"])
        ).fetchone()

    if not application or not application["resume_filename"]:
        abort(404)

    filename = os.path.basename(application["resume_filename"])
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route("/internship/<int:internship_id>/edit", methods=["GET", "POST"])
@role_required("recruiter")
def edit_internship(internship_id):
    with db() as con:
        item = con.execute(
            "SELECT * FROM internships WHERE id=? AND recruiter_id=?",
            (internship_id, session["user_id"])
        ).fetchone()
    if not item:
        flash("Listing not found or you do not own it.", "error")
        return redirect(url_for("dashboard"))
    company_rows = get_companies()
    if request.method == "POST":
        try:
            company = resolve_company_name(request.form)
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("edit_internship", internship_id=internship_id))
        vals = [
            request.form.get("title", "").strip(), company,
            request.form.get("location", "").strip(), request.form.get("mode", "").strip(),
            request.form.get("category", "").strip(), request.form.get("stipend", "").strip(),
            request.form.get("description", "").strip()
        ]
        if not all(vals[i] for i in (0, 1, 2, 3, 4, 6)):
            flash("Please complete all required fields and select a company.", "error")
        else:
            with db() as con:
                con.execute(
                    """UPDATE internships SET title=?,company=?,location=?,mode=?,
                       category=?,stipend=?,description=? WHERE id=? AND recruiter_id=?""",
                    (*vals, internship_id, session["user_id"])
                )
            flash("Listing updated.", "success")
            return redirect(url_for("dashboard"))
    return render_template("internship_form.html", internship=item, companies=company_rows)


@app.route("/internship/<int:internship_id>/delete", methods=["POST"])
@role_required("recruiter")
def delete_internship(internship_id):
    with db() as con:
        cur = con.execute("DELETE FROM internships WHERE id=? AND recruiter_id=?",
                          (internship_id, session["user_id"]))
        changed = cur.rowcount
    flash("Listing deleted." if changed else "Listing not found or not yours.",
          "success" if changed else "error")
    return redirect(url_for("dashboard"))


@app.route("/internship/<int:internship_id>/feature", methods=["POST"])
@role_required("recruiter")
def feature_internship(internship_id):
    with db() as con:
        cur = con.execute(
            """UPDATE internships SET featured=CASE WHEN featured=1 THEN 0 ELSE 1 END
               WHERE id=? AND recruiter_id=?""",
            (internship_id, session["user_id"])
        )
        changed = cur.rowcount
    flash("Featured status updated." if changed else "Listing not found or not yours.",
          "success" if changed else "error")
    return redirect(url_for("dashboard"))


@app.route("/internship/<int:internship_id>/applications")
@role_required("recruiter")
def manage_applications(internship_id):
    with db() as con:
        owned = con.execute(
            "SELECT title FROM internships WHERE id=? AND recruiter_id=?",
            (internship_id, session["user_id"])
        ).fetchone()
        if not owned:
            flash("Listing not found or you do not own it.", "error")
            return redirect(url_for("dashboard"))
        applications = con.execute(
            """SELECT a.*, u.name, u.email FROM applications a
               JOIN users u ON u.id=a.student_id
               WHERE a.internship_id=? ORDER BY a.created_at DESC""",
            (internship_id,)
        ).fetchall()
    return render_template("applications.html", apps=applications,
                           title=owned["title"], internship_id=internship_id)


@app.route("/application/<int:application_id>/status", methods=["POST"])
@role_required("recruiter")
def update_status(application_id):
    status = request.form.get("status")
    allowed = ("Pending", "Reviewed", "Shortlisted", "Rejected", "Accepted")
    if status not in allowed:
        flash("Invalid status.", "error")
        return redirect(url_for("dashboard"))
    with db() as con:
        cur = con.execute(
            """UPDATE applications SET status=? WHERE id=? AND internship_id IN
               (SELECT id FROM internships WHERE recruiter_id=?)""",
            (status, application_id, session["user_id"])
        )
        changed = cur.rowcount
    flash("Application status updated." if changed else "Application not found or not yours.",
          "success" if changed else "error")
    return redirect(request.referrer or url_for("dashboard"))


@app.errorhandler(413)
def file_too_large(_error):
    flash("Resume is too large. Maximum allowed size is 5 MB.", "error")
    return redirect(request.referrer or url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
