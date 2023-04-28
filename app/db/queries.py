from app.db.connection import create_query, create_commit_query

get_doctors = create_query("SELECT * from doctors")

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

get_polyclinics = create_query("SELECT * from polyclinics")

get_patient_history = create_query(
"""
SELECT * from patient_files 
LEFT JOIN patient_tests ON patient_files.record_id=patient_tests.file_id
WHERE owner_id=%s;
"""
)

get_doctor_appointments = create_query(
"""
SELECT patient_id, datetime 
from doctor_appointments where workshift_id 
in (SELECT id from doctor_workshifts where doctor_id=%s);
"""
)

get_doctor_plan = create_query(
"""
SELECT weekday, begin_time, end_time, fio, number, floor, polyclinic_number 
FROM doctor_workshifts
JOIN doctors ON doctor_workshifts.doctor_id=doctors.id
JOIN doctor_offices ON doctor_workshifts.office_id=doctor_offices.id;
WHERE doctor_id=%s
"""
)

get_doctor_test_cost = create_query(
"""
SELECT COALESCE(SUM(cost), 0) FROM patient_tests 
LEFT JOIN doctors_patient_files 
ON patient_tests.file_id=doctors_patient_files.patient_file_record_id
WHERE doctor_id=%s;
"""
)