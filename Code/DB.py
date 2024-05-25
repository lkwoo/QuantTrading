import psycopg2

class DB:
    def DB(self, dbinfo):
        self.dbinfo = dbinfo

    def __enter__(self):
        self.conn = psycopg2.connect(self.dbinfo)
        self.cur = self.conn.cursor()
        return self.conn, self.cur
    
    def __exit__(self):
        self.conn.close()
        self.cur.close()