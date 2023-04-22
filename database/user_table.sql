CREATE TABLE users (
	id serial PRIMARY KEY,
	username VARCHAR (32) UNIQUE NOT NULL,
	password VARCHAR (512) NOT NULL,
	patient_id BIGINT,
	employee_id BIGINT,
	doctor_id BIGINT
);

ALTER TABLE IF EXISTS public.users
    ADD FOREIGN KEY (patient_id)
    REFERENCES public.patients (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.users
    ADD FOREIGN KEY (employee_id)
    REFERENCES public.employees (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.users
    ADD FOREIGN KEY (doctor_id)
    REFERENCES public.doctors (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


INSERT INTO users (username, password, patient_id, employee_id, doctor_id)
VALUES ('admin',
'pbkdf2:sha256:260000$AgE33rU87ikmlpAr$abcf35babeff59ab215d52828af20151537a97806242a8bcaea1b7c6c53196221',
1, 1, 1);

INSERT INTO users (username, password, patient_id, employee_id, doctor_id)
VALUES ('patient',
'pbkdf2:sha256:260000$AgE33rU87ikmlpAr$abcf35babeff59ab215d52828af20151537a97806242a8bcaea1b7c6c53196221',
2, NULL, NULL);

INSERT INTO users (username, password, patient_id, employee_id, doctor_id)
VALUES ('doctor',
'pbkdf2:sha256:260000$AgE33rU87ikmlpAr$abcf35babeff59ab215d52828af20151537a97806242a8bcaea1b7c6c53196221',
NULL, NULL, 3);
