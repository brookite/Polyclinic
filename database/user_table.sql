--TODO: add foreign key
CREATE TABLE users (
	id serial PRIMARY KEY,
	username VARCHAR (32) UNIQUE NOT NULL,
	password VARCHAR (512) NOT NULL,
	patient_id BIGINT,
	employee_id BIGINT,
	doctor_id BIGINT
);

INSERT INTO users (username, password, patient_id, employee_id, doctor_id)
VALUES ('admin', 
		'pbkdf2:sha256:260000$AgE33rU87ikmlpAr$abcf35babeff59ab215d52828af20151537a97806242a8bcaea1b7c6c53196221'
		, 1, 1, 1);