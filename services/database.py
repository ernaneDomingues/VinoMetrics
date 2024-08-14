import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

class Database():
    def __init__(self):
        self.dbname = os.getenv('HDATABASE')
        self.user = os.getenv('HUSER')
        self.password = os.getenv('HPASSWORD')
        self.host = os.getenv('HHOST')
        self.port = os.getenv('HPORT')
        self.schema = 'public'

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, host=self.host, password=self.password)
            self.cur = self.conn.cursor()
        except psycopg2.DatabaseError as e:
            print(f"Error connecting to database: {e}")
            raise
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()

    def execute_query(self, query, params=None):
        try:
            self.cur.execute(query, params)
            if self.cur.description:
                return self.cur.fetchall()
        except psycopg2.DatabaseError as e:
            print(f"Error executing query: {e}")
            raise
        
    def get_items_year(self, table, year):
        if not isinstance(year, int):
            raise ValueError("Year must be an integer")
        query = sql.SQL("""SELECT * FROM {}.{} WHERE ano = %s""").format(sql.Identifier(self.schema), sql.Identifier(table))
        return self.execute_query(query, (year,))
    
    def get_items_between_years(self, table, start_year, end_year):
        if not isinstance(start_year, int) or not isinstance(end_year, int):
            raise ValueError("Start year and end year must be integers")
        query = sql.SQL("""SELECT * FROM {}.{} WHERE ano BETWEEN %s AND %s""").format(sql.Identifier(self.schema), sql.Identifier(table))
        return self.execute_query(query, (start_year, end_year))
