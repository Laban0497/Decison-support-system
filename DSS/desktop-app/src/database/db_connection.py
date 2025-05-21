import sqlite3

def connect_db(db_name="app_database.db"):
    conn = sqlite3.connect(db_name)
    return conn

def disconnect_db(conn):
    if conn:
        conn.close()