import psycopg2
from settings import DATABASE_URL


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def close_db_connection(conn):
    conn.close()
