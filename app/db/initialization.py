from app.db.connection import close_db, connect_db


def init_database_schema():
    filename = "database/main_tables.sql"
    with open(filename, "r", encoding="utf-8") as fobj:
        sql = fobj.read()
        conn, cursor = connect_db()
        cursor.execute(sql)
        close_db(conn, cursor)
