import os

from sql_judge_utils.parser import get_queries

base_dir = os.path.dirname(__file__)
solution_file_path = os.path.join(base_dir, "test_resources/solution_17906.sql")


def test_queries():
    queries = get_queries(solution_file_path)
    print(queries)
    assert len(queries) == 3
    q1 = "\nInsert into Player(id, team, age)\nSelect t.id, 'Chelsea', 24\nFrom (\n\tselect id from Person where id not in (\n\t\tselect id from Player\n\t\tunion\n\t\tselect id from Coach\n\t\tunion\n\t\tselect id from Refree\n\t)\n) as t\n"
    q2 = "\nSelect id, name\nFrom Person\nWhere id in (\n\tselect c.id\n\tfrom Coach as c\n\tleft join Player as p\n\ton p.id=c.id\n\twhere p.team != c.team\n)\n"
    q3 = "\nAlter Table Player\nADD FOREIGN KEY (team) REFERENCES Team(name) ON DELETE CASCADE"
    expected_queries = [q1, q2, q3]
    for i in range(3):
        assert queries[i] == expected_queries[i]
