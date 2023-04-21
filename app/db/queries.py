from app.db.connection import create_query

get_doctors = create_query("SELECT * from doctors LIMIT 30")
get_patients = create_query("SELECT * from patients")
get_current_doctor_workshifts = create_query(
"""SELECT id, doctor_id, office_id from doctor_workshifts 
WHERE weekday=extract(dow from current_date) AND current_time >= begin_time AND current_time < end_time;
"""
)
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
