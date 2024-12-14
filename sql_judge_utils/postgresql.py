import os
from typing import Union

import psycopg2
from psycopg2 import extras
from psycopg2.sql import SQL, Identifier

from sql_judge_utils.database import Database


class PostgresqlDatabase(Database):
    def __init__(
        self,
        db_name: str,
        *,
        host: str = "postgresql",
        port: Union[int, str] = 5432,
        username: str = "postgres",
        password: str = None,
    ):
        super().__init__(db_name, host=host, port=port, username=username, password=password)

    def connect(self):
        connection = psycopg2.connect(user=self.username, password=self.password, host=self.host, port=self.port)
        return connection

    def connect_to_db(self):
        connection = psycopg2.connect(
            dbname=self.db_name, user=self.username, password=self.password, host=self.host, port=self.port
        )
        return connection

    def create(self):
        conn = self.connect()
        conn.autocommit = True
        try:
            cursor = conn.cursor()
            cursor.execute(SQL("CREATE DATABASE {}").format(Identifier(self.db_name)))
            cursor.close()
        finally:
            conn.close()

    def drop(self):
        conn = self.connect()
        conn.autocommit = True
        try:
            cursor = conn.cursor()
            cursor.execute(SQL("DROP DATABASE IF EXISTS {}").format(Identifier(self.db_name)))
            cursor.close()
        finally:
            conn.close()

    def init(self, sql_string: str):
        conn = self.connect_to_db()
        try:
            cursor = conn.cursor()
            cursor.execute(sql_string)
            conn.commit()
            cursor.close()
        finally:
            conn.close()

    def initf(self, sql_file_path, delete_file=False):
        if not os.path.exists(sql_file_path):
            raise Exception(f"SQL file not found: {sql_file_path}")
        with open(sql_file_path) as f:
            sql_string = f.read()
        self.init(sql_string)
        if delete_file:
            os.unlink(sql_file_path)

    def run_query(self, sql_string) -> tuple[list[str], list[list]]:
        """

        :param sql_string:
        :return:
            col_names
            records
        """
        conn = self.connect_to_db()
        conn.autocommit = True
        try:
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
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
        sql = "select table_name from information_schema.tables where table_schema='public'"
        _, records = self.run_query(sql)
        table_names = []
        for row in records:
            table_names.append(row[0])
        return table_names
