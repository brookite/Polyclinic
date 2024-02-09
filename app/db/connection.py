import psycopg2
import psycopg2.extras
import traceback
import os


def connect_db():
    conn = psycopg2.connect(
        dbname=os.getenv("POLYCLINIC_DB_NAME"),
        user=os.getenv("POLYCLINIC_DB_USER"),
        password=os.getenv("POLYCLINIC_DB_PASSWORD"),
        host=os.getenv("POLYCLINIC_DB_HOST"),
    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cursor


def close_db(conn, cursor):
    cursor.close()
    conn.close()


def create_query(query, max_count=None):
    def wrapper(*args):
        db, cursor = connect_db()
        cursor.execute(query, args)
        if max_count:
            result = [dict(ans) for ans in cursor.fetchmany(max_count)]
        else:
            result = [dict(ans) for ans in cursor.fetchall()]
        close_db(db, cursor)
        return result

    return wrapper


def create_commit_query(query):
    def wrapper(*args):
        db, cursor = connect_db()
        try:
            cursor.execute(query, args)
            db.commit()
            result = True
        except:
            traceback.print_exc()
            result = False
        close_db(db, cursor)
        return result

    return wrapper
