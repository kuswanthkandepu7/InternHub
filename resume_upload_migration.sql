USE defaultdb;

ALTER TABLE applications
ADD COLUMN resume_filename VARCHAR(255) NULL;
