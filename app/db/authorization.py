from app.db.connection import connect_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Dict
from app.utils.enums import Role


def get_user(username, cursor=None):
    if not username:
        return None

    if cursor is None:
        conn, cursor_ = connect_db()
    else:
        cursor_ = cursor
    cursor_.execute('SELECT * FROM users WHERE username=%s', (username,))
    account = cursor_.fetchone()
    if cursor is None:
        close_db(conn, cursor_)
    return account


def login_user(username, password):
    account = get_user(username)
    if account:
        account_password = account["password"]
        if check_password_hash(account_password, password):
            return account


def register_user(username, password, roles: Dict[Role, int]):
    conn, cursor = connect_db()

    hashed_password = generate_password_hash(password)

    if not get_user(username, cursor):
        close_db(conn, cursor)
        return False

    cursor.commit(
    """
    INSERT INTO users (username, password)
    VALUES (%s,%s);
    """, (username, hashed_password))

    for role in roles:
        if role == Role.PATIENT:
            field = "patient_id"
        elif role == Role.EMPLOYEE:
            field = "employee_id"
        elif role == Role.DOCTOR:
            field = "doctor_id"
        else:
            raise TypeError(f"Invalid role {role}")
        cursor.commit(
        """
        UPDATE users SET %s=%s WHERE username=%s;
        """, (field, roles[role], username))
    close_db(conn, cursor)


def register_patient(data: Dict):
    username = data["username"]
    password = data["password"]
    
    conn, cursor = connect_db()
    fio = " ".join(data["last_name"], data["first_name"], data["middle_name"])
    cursor.commit(
    """INSERT INTO patients(fio, gender, address, phone_number, birthday, passport_data)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, fio, data["gender"], data["address"], data["phone_number"], 
        data["birthday"], data["passport_data"])
    patient_id = cursor.fetchone(
    """
    SELECT currval(pg_get_serial_sequence('patients','id'))
    """
    )
    close_db(conn, cursor)
    result = register_user(username, password, {Role.PATIENT: patient_id})
    return result


def remove_user(username):
    conn, cursor = connect_db()
    result = False
    if get_user(username, cursor):
        cursor.commit("DELETE FROM users WHERE username=%s", (username,))
        result = True
    close_db(conn, cursor)
    return result


def change_role(username, roles: Dict[Role, int]):
    conn, cursor = connect_db()
    fields = {"patient_id": None, "doctor_id": None, "employee_id": None}
    for role in roles:
        if role == Role.PATIENT:
            field = "patient_id"
        elif role == Role.EMPLOYEE:
            field = "employee_id"
        elif role == Role.DOCTOR:
            field = "doctor_id"
        else:
            raise TypeError(f"Invalid role {role}")
        fields[field] = roles[role]
    cursor.commit(
    """
    UPDATE users
    SET patient_id=%s, 
    SET doctor_id=%s
    SET employee_id=%s WHERE username=%s;
    """, (fields["patient_id"], fields["doctor_id"], fields["employee_id"], username))
    close_db(conn, cursor)


def get_roles(username) -> Dict[Role, int]:
    account = get_user(username)
    result = {}
    if account:
        if account["patient_id"]:
            result[Role.PATIENT] = account["patient_id"]
        if account["employee_id"]:
            result[Role.EMPLOYEE] = account["employee_id"]
        if account["doctor_id"]:
            result[Role.DOCTOR] = account["doctor_id"]
    return result
