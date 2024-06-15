import psycopg2
from io import StringIO
import pandas as pd

class DatabaseConnection:
    def __init__(self, dbinfo):
        self.dbinfo = dbinfo
        self.conn = None

    def __enter__(self):
        self.conn = psycopg2.connect(self.dbinfo)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

class DatabaseManager(DatabaseConnection):
    def __init__(self, dbinfo):
        '''
        dbinfo: ex) DBINFO = 'postgresql://postgres:asd123123@localhost:5432/stock'
        '''
        super().__init__(dbinfo)
        self.dbinfo = dbinfo

    def get_conn(self):
        return psycopg2.connect(self.dbinfo)

    def fetch_all(self, query):
        with self as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(query)
                    return cur.fetchall()
                except Exception as e:
                    print(f"[Error: fetch_all] {query}\n\n{e}")
                    return

    def fetch_one(self, query):
        with self as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(query)
                    return cur.fetchone()
                except Exception as e:
                    print(f"[Error: fetch_one] {query}\n\n{e}")
                    return

    def execute_query(self, query):
        with self as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(query)
                    conn.commit()
                    return cur.rowcount
                except Exception as e:
                    print(f"[Error: execute_query] {query}\n\n{e}")
                    return
                
    def copy_from_csv_buffer(self, buffer, table_name, sep, columns):
        buffer.seek(0)

        with self as conn:
            with conn.cursor() as cur:
                try:
                    cur.copy_from(file=buffer, table=table_name, columns=columns, sep=sep)
                    conn.commit()
                    return cur.rowcount
                except Exception as e:
                    print(f"[Error: copy_from_csv_buffer] {e}")
                    return

if __name__ == '__main__':
    pass