import psycopg2
from psycopg2 import extras
from sql_judge_utils.database import Database
from typing import List


class PostgresqlDatabase(Database):
    host = '127.0.0.1'
    port = '5432'
    username = 'postgres'
    password = None
    db_name = None

    def connect(self):
        connection = psycopg2.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return connection

    def connect_to_db(self):
        connection = psycopg2.connect(
            database=self.db_name,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return connection

    def create(self):
        conn = self.connect()
        conn.autocommit = True
        cursor = conn.cursor()
        sql = '''CREATE DATABASE %s''' % self.db_name
        cursor.execute(sql)
        conn.close()

    def drop(self):
        conn = self.connect()
        conn.autocommit = True
        cursor = conn.cursor()
        sql = '''DROP DATABASE IF EXISTS %s''' % self.db_name
        cursor.execute(sql)
        conn.close()

    def init(self, sql_string):
        conn = self.connect_to_db()
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql_string)
        print("init successfully.")
        conn.close()

    def run_query(self, sql_string) -> (List[str], List[List]):
        '''

        :param sql_string:
        :return:
            col_names
            records
        '''
        conn = self.connect_to_db()
        conn.autocommit = True
        cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute(sql_string)
        results = cursor.fetchall()
        col_names, records = [], []
        if results:
            col_names = list(results[0].keys())
            records = [list(row.values()) for row in results]

        return col_names, records

    def get_public_table_names(self):
        sql = "select table_name from information_schema.tables where table_schema='public'"
        _, records = self.run_query(sql)
        table_names = []
        for row in records:
            table_names.append(row[0])
        return table_names


