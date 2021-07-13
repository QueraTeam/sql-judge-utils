import os
from typing import List


class Database:
    host = '127.0.0.1'
    port = None
    username = None
    password = None
    db_name = None
    # Fill in child classes
    shell_command = None
    shell_execute_flag = None

    def __init__(self, db_name, **kwargs):
        self.db_name = db_name
        for key in ['host', 'port', 'username', 'password']:
            if key in kwargs:
                setattr(self, key, kwargs.get(key))

    def get_shell_args(self):
        # Fill in child classes
        shell_args = dict(
            host=f'-h {self.host}',
            port=None,
            username=None,
            password=None,
            db_name=None
        )
        return shell_args

    def connect(self):
        raise NotImplementedError

    def connect_to_db(self):
        raise NotImplementedError

    def create(self):
        raise NotImplementedError

    def drop(self):
        raise NotImplementedError

    def get_shell_args_string(self):
        parts = []
        for key, arg_str in self.get_shell_args().items():
            if getattr(self, key) and arg_str:
                parts.append(str(arg_str))
        return ' '.join(parts)

    def init(self, sql_string: str):
        sql_string = " ".join(sql_string.split())
        arg_string = self.get_shell_args_string()
        command = f'{self.shell_command} {arg_string} {self.shell_execute_flag} "{sql_string}"'
        print(command)
        os.system(command)

    def initf(self, sql_file_path):
        arg_string = self.get_shell_args_string()
        command = f"cat {sql_file_path} | {self.shell_command} {arg_string}"
        print(command)
        os.system(command)

    def run_query(self, sql_string) -> (List[str], List[List]):
        '''

        :param sql_string:
        :return:
            col_names
            records
        '''
        raise NotImplementedError

    def get_public_table_names(self):
        raise NotImplementedError

    @staticmethod
    def compare_query_result(first_col_names, first_records, second_col_names, second_records):
        status, message = True, ''

        if len(first_col_names) != len(second_col_names):
            message = 'length of column names are not equal'
            return False, message
        col_count = len(first_col_names)
        for i in range(col_count):
            if first_col_names[i] != second_col_names[i]:
                message = f'column names are not match at index: {i} - {first_col_names[i]} != {second_col_names[i]}'
                return False, message

        if len(first_records) != len(second_records):
            message = 'length of records are not equal'
            return False, message
        rec_count = len(first_records)
        for i in range(rec_count):
            row1 = first_records[i]
            row2 = second_records[i]
            if len(row1) != len(row2):
                message = f'length of rows are not equal at index: {i}'
                return False, message
            for j in range(col_count):
                if row1[j] != row2[j]:
                    message = f'cell of rows are not match at index: {first_col_names[j]},{i} - {row1[j]} != {row2[j]}'
                    return False, message
        return status, message

    def is_equal_on_table(self, db2, table_name) -> (bool, str):
        first_col_names, first_records = self.run_query("SELECT * from %s" % table_name)
        second_col_names, second_records = db2.run_query("SELECT * from %s" % table_name)
        status, message = self.compare_query_result(first_col_names, first_records, second_col_names, second_records)
        return status, message

    def is_equal(self, db2):
        db2_table_names = db2.get_public_table_names()
        for table_name in db2_table_names:
            status, message = self.is_equal_on_table(db2, table_name)
            if not status:
                return status, message
        status, message = True, ''
        return status, message
