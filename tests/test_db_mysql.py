import os

import pytest
from mysql.connector import ProgrammingError

from sql_judge_utils.mysql import MysqlDatabase

base_dir = os.path.dirname(__file__)
initial_sql_file_path = os.path.join(base_dir, "test_resources/initial_100340.sql")


@pytest.fixture
def db1():
    db = MysqlDatabase("db1", host="127.0.0.1", port=13306, password="password")
    yield db
    db.drop()


@pytest.fixture
def db2():
    db = MysqlDatabase("db2", host="127.0.0.1", port=13306, password="password")
    yield db
    db.drop()


def test_initialize():
    db = MysqlDatabase("db1")
    assert db.db_name == "db1"
    assert db.host == "mysql"
    assert db.port == 3306
    assert db.username == "root"
    assert db.password == None


def test_create(db1):
    db1.drop()
    print("create db1")
    db1.create()
    db1.connect_to_db()


def test_drop(db1):
    db1.drop()
    print("create db1")
    db1.create()
    print("drop db1")
    db1.drop()
    try:
        db1.connect_to_db()
    except Exception as ex:
        print(ex)
        assert isinstance(ex, ProgrammingError)
        assert "Unknown database 'db1'" in str(ex)
        # raise ex


def test_init_and_run_count_query(db1):
    db1.drop()
    print("create db1")
    db1.create()
    print("init db1")
    with open(initial_sql_file_path) as f:
        sql_string = f.read()
    db1.init(sql_string)
    _, tables = db1.get_public_table_names()
    print(f"******* tables: {tables}")
    cols1, rows1 = db1.run_query("select count(*) from employees")
    print(f"****** res1: \n{cols1}\n{rows1}")
    assert rows1[0][0] == 22

    cols2, rows2 = db1.run_query("select count(*) from teams")
    print(f"****** res2: \n{cols2}\n{rows2}")
    assert rows2[0][0] == 10


def test_initf_and_run_count_query(db1):
    db1.drop()
    print("create db1")
    db1.create()
    print("initf db1")
    db1.initf(initial_sql_file_path)
    _, tables = db1.get_public_table_names()
    print(f"******* tables: {tables}")
    cols1, rows1 = db1.run_query("select count(*) from employees")
    print(f"****** res1: \n{cols1}\n{rows1}")
    assert rows1[0][0] == 22

    cols2, rows2 = db1.run_query("select count(*) from teams")
    print(f"****** res2: \n{cols2}\n{rows2}")
    assert rows2[0][0] == 10


def test_initf_and_run_all_rows_query(db1):
    db1.drop()
    print("create db1")
    db1.create()
    print("initf db1")
    db1.initf(initial_sql_file_path)
    cols1, rows1 = db1.run_query("select * from employees")
    print(f"****** res1: \n{cols1}\n{rows1}")
    assert len(rows1) == 22
    for i, t in enumerate(["id", "name", "salary", "team_id"]):
        assert cols1[i] == t
    rec5 = rows1[4]
    for i, v in enumerate([5, "andersson", 40000, 1]):
        assert rec5[i] == v

    cols2, rows2 = db1.run_query("select * from teams")
    print(f"****** res2: \n{cols2}\n{rows2}")
    assert len(rows2) == 10
    for i, t in enumerate(["id", "name"]):
        assert cols2[i] == t
    rec5 = rows2[4]
    for i, v in enumerate([5, "app"]):
        assert rec5[i] == v


def test_initf_in_two_db_and_compare_them(db1, db2):
    db1.drop()
    print("create db1")
    db1.create()
    print("initf db1")
    db1.initf(initial_sql_file_path)

    db2.drop()
    print("create db2")
    db2.create()
    print("initf db2")
    db2.initf(initial_sql_file_path)

    print("compare db1 and db2")
    status, message = db1.is_equal(db2)
    assert message == ""
    assert status
