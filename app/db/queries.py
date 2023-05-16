from app.db.connection import create_query, create_commit_query

# common queries

get_doctors_full = create_query("SELECT * from doctors")

get_doctors = create_query("SELECT id, fio, specialization, category from doctors")

get_doctor_by_id = create_query("SELECT * from doctors WHERE id=%s")

get_patients = create_query("SELECT * from patients")

get_patient_by_id = create_query("SELECT * from patients WHERE id=%s")

get_doctors_by_specialization = create_query("SELECT * from doctors WHERE specialization=%s")

get_doctor_workshifts = create_query(
"SELECT id, office_id, weekday, begin_time, end_time from doctor_workshifts WHERE doctor_id=%s;")

get_doctor_workshifts_by_day = create_query(
"SELECT id, office_id, begin_time, end_time from doctor_workshifts WHERE doctor_id=%s AND weekday=%s;")

get_current_doctor_workshifts = create_query(
"""SELECT id, office_id, weekday, begin_time, end_time from doctor_workshifts 
WHERE weekday=extract(dow from current_date) AND current_time >= begin_time AND current_time < end_time;
"""
)

get_appointments_at_workshift = create_query(
"""
SELECT datetime from doctor_appointments WHERE workshift_id=%s
"""
)

get_polyclinics = create_query("SELECT * from polyclinics")

# patient queries

create_appointment = create_commit_query(
"""
INSERT INTO doctor_appointments 
(datetime, workshift_id, patient_id) 
VALUES (%s, %s, %s);
"""
)

check_appointment_free = create_query(
"""
SELECT * from doctor_appointments
WHERE datetime=%s AND workshift_id=%s
"""
)

get_patient_history = create_query(
"""
SELECT STRING_AGG (
	pfm.medicament_name,
        ','
       ORDER BY
        pfm.medicament_name
    ) medicines, 
 	STRING_AGG (
	d.name,
        ','
       ORDER BY
        d.name
    ) diseases, 
	symptoms, treatment_course, 
	record_id,
	first_visit, recovery_date, pt.name AS test_name, 
	pt.cost AS test_cost,
	pt.datetime AS test_datetime,
	doc.id AS doctor_id,
	doc.fio AS doctor_fio,
	doc.specialization AS doctor_specialization
FROM patient_files 
LEFT JOIN patient_tests pt
ON patient_files.record_id=pt.file_id
LEFT JOIN doctors_patient_files dpf
ON dpf.patient_file_record_id=patient_files.record_id
LEFT JOIN patient_files_diseases pfd
ON pfd.patient_file_record_id=patient_files.record_id
LEFT JOIN patient_files_medicaments pfm
ON pfm.patient_file_record_id=patient_files.record_id
LEFT JOIN diseases d
ON pfd.disease_id=d.id
LEFT JOIN doctors doc
ON dpf.doctor_id=doc.id
WHERE owner_id=%s
GROUP BY record_id, symptoms, treatment_course, first_visit, 
recovery_date, test_name, doc.id, test_cost, test_datetime, 
doctor_fio, doctor_specialization;
"""
)

get_patient_appointments = create_query(
"""
SELECT * from doctor_appointments
JOIN doctor_workshifts ON doctor_appointments.workshift_id=doctor_workshifts.id
JOIN doctors ON doctor_workshifts.doctor_id=doctors.id
JOIN doctor_offices ON doctor_workshifts.office_id=doctor_offices.id
WHERE patient_id=%s
ORDER BY datetime;
"""
)

# doctor queries

get_doctor_appointments = create_query(
"""
SELECT patient_id, fio, datetime 
from doctor_appointments
JOIN patients ON patients.id=doctor_appointments.patient_id
where workshift_id in (SELECT id from doctor_workshifts where doctor_id=%s)
;
"""
)

get_doctor_plan = create_query(
"""
SELECT weekday, begin_time, end_time, number, floor, polyclinic_number 
FROM doctor_workshifts
JOIN doctors ON doctor_workshifts.doctor_id=doctors.id
JOIN doctor_offices ON doctor_workshifts.office_id=doctor_offices.id
WHERE doctor_id=%s;
"""
)

get_medicaments = create_query(
"""
SELECT * from medicaments;
"""
)

get_diseases = create_query(
"""
SELECT * from diseases;
"""
)

get_disease_by_name = create_query(
"""
SELECT name, id from diseases WHERE name=%s;
"""
)

get_doctor_patient_history = create_query(
"""
SELECT record_id, p.fio, p.phone_number, STRING_AGG (
	pfm.medicament_name,
        ','
       ORDER BY
        pfm.medicament_name
    ) medicines, 
 	STRING_AGG (
	d.name,
        ','
       ORDER BY
        d.name
    ) diseases, 
	symptoms, treatment_course, 
	record_id, patient_files.owner_id, 
	first_visit, recovery_date, 
    STRING_AGG (
	pt.name,
        ', '
       ORDER BY
        pt.name
    ) test_name,
	STRING_AGG (
	to_char (pt.datetime, 'YYYY-MM-DD HH24:MI:SS'),
        ', '
       ORDER BY
        pt.datetime
    ) test_datetime
FROM patient_files 
LEFT JOIN patient_tests pt
ON patient_files.record_id=pt.file_id
LEFT JOIN patients p ON patient_files.owner_id=p.id
LEFT JOIN doctors_patient_files dpf
ON dpf.patient_file_record_id=patient_files.record_id
LEFT JOIN patient_files_diseases pfd
ON pfd.patient_file_record_id=patient_files.record_id
LEFT JOIN patient_files_medicaments pfm
ON pfm.patient_file_record_id=patient_files.record_id
LEFT JOIN diseases d
ON pfd.disease_id=d.id
LEFT JOIN doctors doc
ON dpf.doctor_id=doc.id
WHERE doc.id=%s
GROUP BY record_id, p.fio, p.phone_number, symptoms, treatment_course, first_visit, 
recovery_date, patient_files.owner_id;
"""
)

edit_patient_record = create_commit_query(
"""
UPDATE patient_files SET 
symptoms=%s,
treatment_course=%s,
recovery_date=%s
WHERE record_id=%s;
"""
)

create_patient_record = create_commit_query(
"""
INSERT INTO patient_files(symptoms, treatment_course, first_visit, owner_id)
VALUES (%s, %s, %s, %s);
INSERT INTO doctors_patient_files(patient_file_record_id, doctor_id)
VALUES ((SELECT currval(pg_get_serial_sequence('patient_files','record_id'))), %s);
"""
)

remove_medicaments_for_record = create_commit_query(
"""
DELETE FROM patient_files_medicaments WHERE patient_file_record_id=%s
"""
)

remove_diseases_for_record = create_commit_query(
"""
DELETE FROM patient_files_diseases WHERE patient_file_record_id=%s
"""
)

add_medicament_to_record = create_commit_query(
"""
INSERT INTO patient_files_medicaments(patient_file_record_id, medicament_name)
VALUES (%s, %s);
"""
)


add_disease_to_record = create_commit_query(
"""
INSERT INTO patient_files_diseases(patient_file_record_id, disease_id)
VALUES (%s, %s);
"""
)

get_last_record_id = create_query(
"""
SELECT max(record_id) AS last_record_id FROM patient_files WHERE owner_id=%s;
"""
)

create_test = create_commit_query(
"""
INSERT INTO patient_tests(name, datetime, cost, file_id)
VALUES (%s, %s, %s, %s);
"""
)

# admin

get_test_cost = create_query(
"""
SELECT COALESCE(SUM(cost), 0) AS cost FROM patient_tests 
LEFT JOIN doctors_patient_files 
ON patient_tests.file_id=doctors_patient_files.patient_file_record_id;
"""
)

get_current_patient_count = create_query(
"""
SELECT COUNT(*) AS patient_count FROM patient_files WHERE recovery_date is NULL;
"""
)

get_avg_recovery_time = create_query(
"""
SELECT avg(recovery_date - first_visit) AS avg_recovery_time FROM patient_files_diseases 
JOIN patient_files ON patient_files_diseases.patient_file_record_id=patient_files.record_id
WHERE recovery_date IS NOT NULL;
"""
)

get_disease_stats = create_query(
"""
SELECT disease_id, diseases.name AS name, COUNT(*) AS disease_count from patient_files 
JOIN patient_files_diseases ON patient_files.record_id=patient_files_diseases.patient_file_record_id 
JOIN diseases ON diseases.id=patient_files_diseases.disease_id
GROUP BY disease_id, diseases.name ORDER BY disease_id ASC;
"""
)

add_new_doctor = create_commit_query(
"""
INSERT INTO doctors (fio, specialization, category, passport_data)
VALUES (%s, %s, %s, %s);
"""
)

remove_doctor = create_commit_query(
"""
DELETE FROM doctor_appointments WHERE workshift_id IN 
	(SELECT id FROM doctor_workshifts WHERE doctor_id = %s);
DELETE FROM doctor_workshifts WHERE doctor_id = %s;
DELETE FROM doctors_polyclinics WHERE doctor_id = %s;
DELETE FROM doctors_patient_files WHERE doctor_id = %s;
DELETE FROM doctors WHERE id=%s
"""
)

add_new_employee = create_commit_query(
"""
INSERT INTO employees (fio, birthdate, address, employment_date, passport_data, post)
VALUES (%s, %s, %s, %s, %s, %s);
"""
)

edit_employee = create_commit_query(
"""
UPDATE employees SET 
fio=%s,
birthdate=%s,
address=%s,
passport_data=%s,
post=%s
WHERE id=%s;
"""
)

get_doctor_offices = create_query(
"""
SELECT id, floor, number, polyclinic_number FROM doctor_offices;
"""
)

add_doctor_office = create_commit_query(
"""
INSERT INTO doctor_offices (number, floor, polyclinic_number) VALUES (%s, %s, %s);
"""
)

remove_doctor_office = create_commit_query(
"""
DELETE FROM doctor_workshifts WHERE office_id=%s;
DELETE FROM doctor_offices WHERE id=%s;
"""
)

add_new_disease = create_commit_query(
"""
INSERT INTO diseases (name) values (%s);
"""
)

get_disease_names = create_query(
"""
SELECT name from diseases;
"""
)

get_medicaments = create_query(
"""
SELECT name, contraindications, indications FROM medicaments;
"""
)

add_new_medicament = create_commit_query(
"""
INSERT INTO medicaments (name, contraindications, indications) 
VALUES (%s, %s, %s);
"""
)

get_employees = create_query(
"""
SELECT * from employees;
"""
)

add_disease_to_medicament = create_commit_query(
"""
INSERT INTO diseases_medicaments(disease_id, medicament_name) 
VALUES (%s, %s)
"""
)

get_workshifts = create_query(
"""
SELECT doctor_workshifts.id, weekday, begin_time, end_time, polyclinic_number, floor, number FROM doctor_workshifts
LEFT JOIN doctor_offices ON doctor_workshifts.office_id=doctor_offices.id
WHERE doctor_id=%s
"""
)

add_workshift = create_commit_query(
"""
INSERT INTO doctor_workshifts 
(weekday, begin_time, end_time, doctor_id, office_id)
VALUES (%s, %s, %s, %s, %s);
"""
)

remove_workshift = create_commit_query(
"""
DELETE FROM doctor_workshifts WHERE id=%s;
"""
)

change_workshift = create_commit_query(
"""
UPDATE doctor_workshifts SET 
begin_time =%s,
end_time=%s,
doctor_id=%s,
office_id=%s
WHERE id=%s;
"""
)