import os
import unittest
import psycopg2
from mysql.connector import ProgrammingError
from sql_judge_utils.mysql import MysqlDatabase
from sql_judge_utils.postgresql import PostgresqlDatabase


class PostgresqlDatabaseTests(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(__file__)
        self.initial_sql_file_path = os.path.join(self.base_dir, 'test_resources/initial_100340.sql')

        options = dict(host='127.0.0.1')
        self.db1 = PostgresqlDatabase('db1', **options)
        self.db2 = PostgresqlDatabase('db2', **options)

    # def tearDown(self):
    #     self.db1.drop()
    #     print("tearDown: db1 drop successfully.")
    #     self.db2.drop()
    #     print("tearDown: db2 drop successfully.")

    def test_create(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        self.db1.connect_to_db()

    def test_drop(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("drop db1")
        self.db1.drop()
        try:
            self.db1.connect_to_db()
        except Exception as ex:
            # print(ex)
            self.assertIsInstance(ex, psycopg2.OperationalError)
            self.assertEqual(str(ex), 'FATAL:  database "db1" does not exist\n')
            # raise ex

    def test_init_and_run_count_query(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("init db1")
        with open(self.initial_sql_file_path) as f:
            sql_string = f.read()
        self.db1.init(sql_string)
        _, tables = self.db1.get_public_table_names()
        print(f"******* tables: {tables}")
        # self.assertIsInstance(tables, list)
        # self.assertEqual(len(tables), 2)
        cols1, rows1 = self.db1.run_query("select count(*) from employees")
        print(f"****** res1: \n{cols1}\n{rows1}")
        self.assertEqual(rows1[0][0], 22)
        # ===
        cols2, rows2 = self.db1.run_query("select count(*) from teams")
        print(f"****** res2: \n{cols2}\n{rows2}")
        self.assertEqual(rows2[0][0], 10)

    def test_initf_and_run_count_query(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("initf db1")
        self.db1.initf(self.initial_sql_file_path)
        _, tables = self.db1.get_public_table_names()
        print(f"******* tables: {tables}")
        # self.assertIsInstance(tables, list)
        # self.assertEqual(len(tables), 2)
        cols1, rows1 = self.db1.run_query("select count(*) from employees")
        print(f"****** res1: \n{cols1}\n{rows1}")
        self.assertEqual(rows1[0][0], 22)
        # ===
        cols2, rows2 = self.db1.run_query("select count(*) from teams")
        print(f"****** res2: \n{cols2}\n{rows2}")
        self.assertEqual(rows2[0][0], 10)

    def test_initf_and_run_all_rows_query(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("initf db1")
        self.db1.initf(self.initial_sql_file_path)
        cols1, rows1 = self.db1.run_query("select * from employees")
        print(f"****** res1: \n{cols1}\n{rows1}")
        self.assertEqual(len(rows1), 22)
        for i, t in enumerate(['id', 'name', 'salary', 'team_id']):
            self.assertEqual(cols1[i], t)
        rec5 = rows1[4]
        for i, v in enumerate([5, 'andersson', 40000, 1]):
            self.assertEqual(rec5[i], v)
        # ===
        cols2, rows2 = self.db1.run_query("select * from teams")
        print(f"****** res2: \n{cols2}\n{rows2}")
        self.assertEqual(len(rows2), 10)
        for i, t in enumerate(['id', 'name']):
            self.assertEqual(cols2[i], t)
        rec5 = rows2[4]
        for i, v in enumerate([5, 'app']):
            self.assertEqual(rec5[i], v)

    def test_initf_in_two_db_and_compare_them(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("initf db1")
        self.db1.initf(self.initial_sql_file_path)
        # ===
        self.db2.drop()
        print("create db2")
        self.db2.create()
        print("initf db2")
        self.db2.initf(self.initial_sql_file_path)
        # ===
        print("compare db1 and db2")
        status, message = self.db1.is_equal(self.db2)
        self.assertEqual(message, '')
        self.assertTrue(status)


class MysqlDatabaseTests(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(__file__)
        self.initial_sql_file_path = os.path.join(self.base_dir, 'test_resources/initial_100340.sql')

        options = dict(host='127.0.0.1', username='username', password='password')
        self.db1 = MysqlDatabase('db1', **options)
        self.db2 = MysqlDatabase('db2', **options)

    # def tearDown(self):
    #     self.db1.drop()
    #     print("tearDown: db1 drop successfully.")
    #     self.db2.drop()
    #     print("tearDown: db2 drop successfully.")

    def test_create(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        self.db1.connect_to_db()

    def test_drop(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("drop db1")
        self.db1.drop()
        try:
            self.db1.connect_to_db()
        except Exception as ex:
            print(ex)
            self.assertIsInstance(ex, ProgrammingError)
            self.assertTrue("Unknown database 'db1'" in str(ex))
            # raise ex

    def test_init_and_run_count_query(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("init db1")
        with open(self.initial_sql_file_path) as f:
            sql_string = f.read()
        self.db1.init(sql_string)
        _, tables = self.db1.get_public_table_names()
        print(f"******* tables: {tables}")
        # self.assertIsInstance(tables, list)
        # self.assertEqual(len(tables), 2)
        cols1, rows1 = self.db1.run_query("select count(*) from employees")
        print(f"****** res1: \n{cols1}\n{rows1}")
        self.assertEqual(rows1[0][0], 22)
        # ===
        cols2, rows2 = self.db1.run_query("select count(*) from teams")
        print(f"****** res2: \n{cols2}\n{rows2}")
        self.assertEqual(rows2[0][0], 10)

    def test_initf_and_run_count_query(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("initf db1")
        self.db1.initf(self.initial_sql_file_path)
        _, tables = self.db1.get_public_table_names()
        print(f"******* tables: {tables}")
        # self.assertIsInstance(tables, list)
        # self.assertEqual(len(tables), 2)
        cols1, rows1 = self.db1.run_query("select count(*) from employees")
        print(f"****** res1: \n{cols1}\n{rows1}")
        self.assertEqual(rows1[0][0], 22)
        # ===
        cols2, rows2 = self.db1.run_query("select count(*) from teams")
        print(f"****** res2: \n{cols2}\n{rows2}")
        self.assertEqual(rows2[0][0], 10)

    def test_initf_and_run_all_rows_query(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("initf db1")
        self.db1.initf(self.initial_sql_file_path)
        cols1, rows1 = self.db1.run_query("select * from employees")
        print(f"****** res1: \n{cols1}\n{rows1}")
        self.assertEqual(len(rows1), 22)
        for i, t in enumerate(['id', 'name', 'salary', 'team_id']):
            self.assertEqual(cols1[i], t)
        rec5 = rows1[4]
        for i, v in enumerate([5, 'andersson', 40000, 1]):
            self.assertEqual(rec5[i], v)
        # ===
        cols2, rows2 = self.db1.run_query("select * from teams")
        print(f"****** res2: \n{cols2}\n{rows2}")
        self.assertEqual(len(rows2), 10)
        for i, t in enumerate(['id', 'name']):
            self.assertEqual(cols2[i], t)
        rec5 = rows2[4]
        for i, v in enumerate([5, 'app']):
            self.assertEqual(rec5[i], v)

    def test_initf_in_two_db_and_compare_them(self):
        self.db1.drop()
        print("create db1")
        self.db1.create()
        print("initf db1")
        self.db1.initf(self.initial_sql_file_path)
        # ===
        self.db2.drop()
        print("create db2")
        self.db2.create()
        print("initf db2")
        self.db2.initf(self.initial_sql_file_path)
        # ===
        print("compare db1 and db2")
        status, message = self.db1.is_equal(self.db2)
        self.assertEqual(message, '')
        self.assertTrue(status)


if __name__ == '__main__':
    unittest.main()
