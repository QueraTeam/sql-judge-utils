# sql-judge-utils

Utils methods to write python unit tests for version 2 of [QUERA](https://quera.ir) sql judge system.

## Install

```shell script
pip install sql-judge-utils # or git+https://github.com/QueraTeam/sql-judge-utils
```

---

# Database 
### 1. Import one of database classes
- Postgresql:
```python
from sql_judge_utils.postgresql import PostgresqlDatabase as Database
```
- Mysql:
```python
from sql_judge_utils.mysql import MysqlDatabase as Database
```

### 2. Define database instances:

```python
db1 = Database('db1')
db2 = Database('db2')
```

##### Optional arguments in database defining:
| Option key | Postgresql default | Mysql default | 
|---|---|---|
| `host` | `'postgresql'` | `'mysql'` |
| `port` | `'5432'` | `'3306'` |
| `username` | `'postgres'` | `'root'` |
| `password` | `None` | `None` |

**⚠️ WARNING:**
Dont change these properties in [QUERA](https://quera.ir) judge tests. These must be same default values 

### 3. Use utils:
- Create database:

```python
db1.create()
```

- Drop database:

```python
db1.drop()
```

- Init data with sql string or sql file path:

```python
db1.init(sql_string)
# or
db1.initf(sql_file_path)
```

- Run query

```python
col_names, records = db1.run_query(sql_string)
```

- Compare two result of run_query:

```python
status, message = Database.compare_query_result(col_names_1, records_1, col_names_2, records_2)
```

- Compare two database instances:

```python
status, message = db1.is_equal(db2)
```

- Compare two database instances on a table:

```python
status, message = db1.is_equal_on_table(db2, table_name)
```

---

# SQL parser to find submission queries

```python
from sql_judge_utils.parser import get_queries, get_query
submission_file_path = 'path/to/submission.sql'
queries = get_queries(submission_file_path)
# or
submission_file_path = 'path/to/submission.sql'
query_number = 2
query = get_query(submission_file_path, query_number)
```

--- 
