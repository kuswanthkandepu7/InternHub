-- Run this in Aiven's MySQL Query Editor while connected to defaultdb.
-- The database itself is selected by the Aiven connection URI.

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'recruiter') NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS internships (
    id INT NOT NULL AUTO_INCREMENT,
    recruiter_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    mode VARCHAR(50) NOT NULL,
    category VARCHAR(150) NOT NULL,
    stipend VARCHAR(100) DEFAULT '',
    description TEXT NOT NULL,
    featured TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_internships_recruiter (recruiter_id),
    KEY idx_internships_featured_created (featured, created_at),
    CONSTRAINT fk_internships_recruiter
        FOREIGN KEY (recruiter_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS applications (
    id INT NOT NULL AUTO_INCREMENT,
    internship_id INT NOT NULL,
    student_id INT NOT NULL,
    message TEXT,
    status ENUM('Pending', 'Reviewed', 'Shortlisted', 'Rejected', 'Accepted')
        NOT NULL DEFAULT 'Pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_application_student_internship (internship_id, student_id),
    KEY idx_applications_student (student_id),
    CONSTRAINT fk_applications_internship
        FOREIGN KEY (internship_id) REFERENCES internships(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_applications_student
        FOREIGN KEY (student_id) REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
