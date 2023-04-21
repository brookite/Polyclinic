import psycopg2
import psycopg2.extras


def connect_db():
    conn = psycopg2.connect(dbname='Polyclinic', user='postgres', 
                        password='12345', host='localhost')
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
