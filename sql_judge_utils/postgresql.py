import psycopg2
from psycopg2 import extras

from sql_judge_utils.database import Database


class PostgresqlDatabase(Database):
    def __init__(
        self,
        db_name: str,
        *,
        host: str = "postgresql",
        port: int | str = 5432,
        username: str = "postgres",
        password: str = None,
    ):
        super.__init__(db_name, host=host, port=port, username=username, password=password)

    def connect(self):
        connection = psycopg2.connect(user=self.username, password=self.password, host=self.host, port=self.port)
        return connection

    def connect_to_db(self):
        connection = psycopg2.connect(
            database=self.db_name, user=self.username, password=self.password, host=self.host, port=self.port
        )
        return connection

    def create(self):
        conn = self.connect()
        conn.autocommit = True
        cursor = conn.cursor()
        sql = f"""CREATE DATABASE {self.db_name}"""
        cursor.execute(sql)
        conn.close()

    def drop(self):
        conn = self.connect()
        conn.autocommit = True
        cursor = conn.cursor()
        sql = f"""DROP DATABASE IF EXISTS {self.db_name}"""
        cursor.execute(sql)
        conn.close()

    def run_query(self, sql_string) -> tuple[list[str], list[list]]:
        """

        :param sql_string:
        :return:
            col_names
            records
        """
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

    def get_public_table_names(self) -> list[str]:
        sql = "select table_name from information_schema.tables where table_schema='public'"
        _, records = self.run_query(sql)
        table_names = []
        for row in records:
            table_names.append(row[0])
        return table_names
