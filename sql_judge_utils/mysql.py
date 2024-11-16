import mysql.connector

from sql_judge_utils.database import Database


class MysqlDatabase(Database):
    shell_command = "mysql"
    shell_execute_flag = "-e"

    def __init__(
        self,
        db_name: str,
        *,
        host: str = "mysql",
        port: int | str = 3306,
        username: str = "root",
        password: str = None,
    ):
        super.__init__(db_name, host=host, port=port, username=username, password=password)

    def get_shell_args(self):
        shell_args = dict(
            host=f"-h {self.host}",
            port=f"-P {self.port}",
            username=f"-u {self.username}",
            password=f"--password={self.password}",
            db_name=f"-D {self.db_name}",
        )
        return shell_args

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
        cursor = conn.cursor()
        sql = f"""CREATE DATABASE {self.db_name}"""
        cursor.execute(sql)
        conn.close()

    def drop(self):
        conn = self.connect()
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
        col_names, records = [], []

        conn = self.connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_string)
        results = cursor.fetchall()
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
