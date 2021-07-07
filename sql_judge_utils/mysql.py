from sql_judge_utils.database import Database
from typing import List
import mysql.connector


class MysqlDatabase(Database):
    host = '127.0.0.1'
    port = '3306'
    username = 'username'
    password = 'password'
    db_name = None

    def connect(self):
        connection = mysql.connector.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return connection

    def connect_to_db(self):
        connection = mysql.connector.connect(
            database=self.db_name,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return connection

    def create(self):
        conn = self.connect()
        cursor = conn.cursor()
        sql = '''CREATE DATABASE %s''' % self.db_name
        cursor.execute(sql)
        conn.close()

    def drop(self):
        conn = self.connect()
        cursor = conn.cursor()
        sql = '''DROP DATABASE IF EXISTS %s''' % self.db_name
        cursor.execute(sql)
        conn.close()

    def init(self, sql_string, separate=True):
        conn = self.connect_to_db()
        cursor = conn.cursor()
        # TODO: double check this lines!
        #  Split large sql because not work correctly in mysql
        if separate:
            for sql in sql_string.split(';'):
                sql = ' '.join(sql.split())
                # print(sql)
                if sql:
                    cursor.execute(sql)
                    conn.commit()

        else:
            cursor.execute(sql_string)
            conn.commit()

        conn.close()
        print("init successfully.")

    def run_query(self, sql_string) -> (List[str], List[List]):
        '''

        :param sql_string:
        :return:
            col_names
            records
        '''
        col_names, records = [], []

        conn = self.connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_string)
        results = cursor.fetchall()
        if results:
            col_names = list(results[0].keys())
            records = [list(row.values()) for row in results]

        return col_names, records

    def get_public_table_names(self):
        sql = "show tables"
        _, records = self.run_query(sql)
        table_names = []
        for row in records:
            table_names.append(row[0])
        return table_names


