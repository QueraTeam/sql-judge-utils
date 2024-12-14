import os
import subprocess
from tempfile import NamedTemporaryFile
from typing import Union

import mysql.connector

from sql_judge_utils.database import Database


class MysqlDatabase(Database):
    def __init__(
        self,
        db_name: str,
        *,
        host: str = "mysql",
        port: Union[int, str] = 3306,
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
        with NamedTemporaryFile() as fp:
            fp.write(sql_string.encode("utf-8"))
            fp.flush()
            self.initf(fp.name)

    def initf(self, sql_file_path, delete_file=False):
        """
        We rely on the external "mysql" command instead of using the Python package "mysql.connector".
        The reason is that mysql.connector can only execute single queries at a time, not a script
        with multiple queries. We tried using "sqlparse" to split the script into separate queries and
        execute them individually, but it was not reliable because some queries need to be executed in
        a single session. Additionally, for large scripts (e.g., 20MB), sqlparse execution was
        extremely slow. Therefore, we have no choice but to depend on the "mysql" command.
        """
        if not os.path.exists(sql_file_path):
            raise Exception(f"SQL file not found: {sql_file_path}")
        with open(sql_file_path) as fp:
            subprocess.run(
                [
                    "mysql",
                    f"-h{self.host}",
                    f"-P{self.port}",
                    f"-u{self.username}",
                    f"--password={self.password}",
                    f"-D{self.db_name}",
                ],
                stdin=fp,
            )
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
