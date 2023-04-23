from app.db.connection import create_query

get_doctors = create_query("SELECT * from doctors")
get_patients = create_query("SELECT * from patients")
get_patient_by_id = create_query("SELECT * from patients WHERE id=%s")
get_doctors_by_specialization = create_query("SELECT * from doctors WHERE specialization=%s")

get_doctor_workshifts = create_query(
"SELECT id, office_id, weekday, begin_time, end_time from doctor_workshifts WHERE doctor_id=%s;")

get_current_doctor_workshifts = create_query(
"""SELECT id, office_id, weekday, begin_time, end_time from doctor_workshifts 
WHERE weekday=extract(dow from current_date) AND current_time >= begin_time AND current_time < end_time;
"""
)

get_polyclinics = create_query("SELECT * from polyclinics")

get_patient_history = create_query(
"""
SELECT record_id, symptoms, first_visit, recovery_date from patient_files WHERE owner_id=%s;
"""
)
get_patient_history = create_query(
"""
SELECT record_id, symptoms, first_visit, recovery_date from patient_files WHERE owner_id=%s;
"""
)
