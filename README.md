# InternHub – Aiven MySQL Edition

InternHub is a Flask internship platform with student/recruiter roles, internship listings, applications, recruiter ownership checks, and application status tracking.

## Stack
- Python + Flask
- Aiven MySQL
- mysql-connector-python
- HTML/CSS/Jinja templates

## 1. Create the Aiven tables
1. Open your Aiven Console and select your MySQL service.
2. Open the SQL Query Editor for the `defaultdb` database (or the database name in your URI).
3. Open `schema.sql` from this project, copy all its SQL, paste it into the editor, and execute it.
4. Confirm that `users`, `internships`, and `applications` tables exist.

Do not run the schema in a different database from the one in `DATABASE_URL`.

## 2. Install Python dependencies
Open PowerShell in the folder containing `app.py`:

```powershell
python -m pip install -r requirements.txt
```

## 3. Set your Aiven URI in PowerShell
Use the actual connection URI from Aiven, but keep it private:

```powershell
$env:DATABASE_URL = "mysql://USERNAME:PASSWORD@HOST:PORT/defaultdb?ssl-mode=REQUIRED"
```

Replace the example with your real URI. Do not type the masked example URI; it cannot connect.

For stronger TLS server verification, download the CA certificate from your Aiven service, then set:

```powershell
$env:MYSQL_SSL_CA = "C:\path\to\ca.pem"
```

The app always uses TLS (`ssl_disabled=False`). When `MYSQL_SSL_CA` is set, it also verifies the certificate and hostname.

Optional session secret:

```powershell
$env:SECRET_KEY = "replace-with-a-long-random-value"
```

Environment variables set this way apply to the current PowerShell window. Set them again in a new terminal session.

## 4. Start the application

```powershell
python app.py
```

Open http://127.0.0.1:5000

## 5. Test the workflow
1. Register a recruiter account.
2. Sign in as recruiter and publish an internship.
3. Register a student account (use a different email).
4. Sign in as student, browse, and apply.
5. Sign back in as recruiter to view applications and update statuses.
6. Sign in as student to view the updated application status.

## Project structure

```text
InternHub/
├── app.py
├── schema.sql
├── requirements.txt
├── .env.example
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── student_dashboard.html
    ├── recruiter_dashboard.html
    ├── internship_form.html
    ├── detail.html
    └── applications.html
```

## Security and deployment notes
- Passwords are stored as Werkzeug hashes.
- SQL queries use parameterized values.
- Recruiter-only routes and ownership checks are enforced server-side.
- Keep `DATABASE_URL`, `SECRET_KEY`, and the CA file private; never commit credentials.
- Use a production WSGI server, HTTPS, CSRF protection, rate limiting, secure cookies, and backups before public deployment.
- Debug mode is enabled by the development `app.run()` entry point; do not expose the development server publicly.
