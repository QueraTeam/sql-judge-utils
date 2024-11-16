import mysql.connector
import sqlparse

from sql_judge_utils.database import Database


class MysqlDatabase(Database):
    def __init__(
        self,
        db_name: str,
        *,
        host: str = "mysql",
        port: int | str = 3306,
        username: str = "root",
        password: str = None,
    ):
        super().__init__(db_name, host=host, port=port, username=username, password=password)

    def connect(self):
        connection = mysql.connector.connect(user=self.username, password=self.password, host=self.host, port=self.port)
        return connection

    def connect_to_db(self):
        connection = mysql.connector.connect(
            database=self.db_name, user=self.username, password=self.password, host=self.host, port=self.port
        )
        return connection

    def create(self):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {self.db_name}")
            cursor.close()
        finally:
            conn.close()

    def drop(self):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
            cursor.close()
        finally:
            conn.close()

    def init(self, sql_string: str):
        conn = self.connect_to_db()
        try:
            cursor = conn.cursor()
            # In MySQL we can't execute multiple statements in one go.
            for statement in sqlparse.split(sql_string):
                cursor.execute(statement)
            conn.commit()
            cursor.close()
        finally:
            conn.close()

    def run_query(self, sql_string) -> tuple[list[str], list[list]]:
        """

        :param sql_string:
        :return:
            col_names
            records
        """
        conn = self.connect_to_db()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql_string)
            results = cursor.fetchall()
            cursor.close()
        finally:
            conn.close()

        col_names, records = [], []
        if results:
            col_names = list(results[0].keys())
            records = [list(row.values()) for row in results]
        return col_names, records

    def get_public_table_names(self) -> list[str]:
        sql = "show tables"
        _, records = self.run_query(sql)
        table_names = []
        for row in records:
            table_names.append(row[0])
        return table_names
