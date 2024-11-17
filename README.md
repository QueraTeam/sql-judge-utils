# sql-judge-utils

Utilities for writing Python unit tests for version 2 of the [Quera](https://quera.ir) SQL judge.

## Installation

```shell
pip install sql-judge-utils # or git+https://github.com/QueraTeam/sql-judge-utils
```

## Usage

Import one of database classes:

```python
# PostgreSQL:
from sql_judge_utils.postgresql import PostgresqlDatabase as Database

# MySQL:
from sql_judge_utils.mysql import MysqlDatabase as Database
```

Define database instances:

```python
db1 = Database("db1")
db2 = Database("db2")
```

Optional arguments:

| Argument   | PostgreSQL default | MySQL default |
| ---------- | ------------------ | ------------- |
| `host`     | `"postgresql"`     | `"mysql"`     |
| `port`     | `5432`             | `3306`        |
| `username` | `"postgres"`       | `"root"`      |
| `password` | `None`             | `None`        |

> **WARNING:**
> Don't override the default values
> if you're writing tests for [Quera](https://quera.ir) SQL judge.

Create database:

```python
db1.create()
```

Drop database:

```python
db1.drop()
```

Init data (run SQL command without fetching results)
with SQL string or SQL file path:

```python
db1.init(sql_string)
# or
db1.initf(sql_file_path)
```

Run query and fetch the results:

```python
col_names, records = db1.run_query(sql_string)
```

Compare two result of run_query:

```python
status, message = Database.compare_query_result(col_names_1, records_1, col_names_2, records_2)
```

Compare two database instances:

```python
status, message = db1.is_equal(db2)
```

Compare two database instances on a table:

```python
status, message = db1.is_equal_on_table(db2, table_name)
```



### Submission parser

Use the parser to extract queries from a submission file:

```python
from sql_judge_utils.parser import get_queries, get_query
submission_file_path = 'path/to/submission.sql'
queries = get_queries(submission_file_path)
# or
submission_file_path = 'path/to/submission.sql'
query_number = 2
query = get_query(submission_file_path, query_number)
```

## Development

Install Hatch and pre-commit hooks:

```shell
pipx install hatch
pipx install pre-commit
pre-commit install
```

Before running the tests, start a MySQL and a PostgreSQL instance:

```shell
docker run --name sql-postgres -e POSTGRES_PASSWORD=password -p "127.0.0.1:15432:5432" -d postgres postgres -c log_statement=all
docker run --name sql-mysql -e MYSQL_ROOT_PASSWORD=password -p "127.0.0.1:13306:3306" -d mysql
```

Run the tests and stop the database instances:

```shell
hatch test --all
docker stop sql-postgres sql-mysql
docker rm sql-postgres sql-mysql
```

Build and publish:

```shell
hatch build
hatch publish
```
