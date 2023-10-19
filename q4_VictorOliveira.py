from mysql.connector import connect
from datetime import date, datetime

# Constants
MYSQL_CREDENTIALS = lambda: {"host": "localhost", "user": "root", "password": "root"}
DATABASE_NAME = lambda: "functional_programming"

# Functions
# - Messages
question_title = lambda: print("QUESTION 04 BY VICTOR KAUAN LIMA DE OLIVEIRA")

# - General
comma_concat = lambda iterable: ", ".join([str(item) for item in iterable])

# - MySQL
# -- General
connect_database = lambda host, user, password: connect(host=host, user=user, password=password)
create_cursor = lambda database: database.cursor()
run_sql_command = lambda cursor, command: cursor.execute(command)
fetch_all = lambda cursor: cursor.fetchall()

# -- DDL
create_database = lambda database, cursor, if_not_exists=False: run_sql_command(
    cursor=cursor,
    command=f"CREATE DATABASE {'IF NOT EXISTS' if if_not_exists else ''} {database};",
)
drop_database = lambda database, cursor: run_sql_command(cursor=cursor, command=f"DROP DATABASE {database};")
use_database = lambda database, cursor: run_sql_command(cursor=cursor, command=f"USE {database};")

create_table = lambda table, attributes, cursor, if_not_exists=False: run_sql_command(
    cursor=cursor,
    command=f"CREATE TABLE {'IF NOT EXISTS' if if_not_exists else ''} {table} ({comma_concat(attributes)});",
)
drop_table = lambda table, cursor: run_sql_command(cursor=cursor, command=f"DROP TABLE {table};")

# -- DML
insert_into = lambda table, attributes, values, cursor: run_sql_command(
    cursor=cursor,
    command="INSERT INTO {} ({}) VALUES {};".format(
        table,
        comma_concat(attributes),
        comma_concat([f"'{value}'" if type(value) in (str, date, datetime) else value for value in values]),
    ),
)
delete_from_where = lambda table, conditions, cursor: run_sql_command(
    cursor=cursor,
    command=f"DELETE FROM {table} WHERE {conditions};",
)
select_from_where = lambda table, attributes, cursor, conditions=None: run_sql_command(
    cursor=cursor,
    command=f"SELECT {comma_concat(attributes)} FROM {table} {f'WHERE {conditions}' if conditions else ''};",
)

question_title()

# MySQL connection
mysql_database = connect_database(**MYSQL_CREDENTIALS())
mysql_cursor = create_cursor(database=mysql_database)

# Create database
create_database(database=DATABASE_NAME(), cursor=mysql_cursor, if_not_exists=True)
use_database(database=DATABASE_NAME(), cursor=mysql_cursor)

# Create tables
create_table(
    table="usuarios",
    attributes=("id INT AUTO_INCREMENT PRIMARY KEY", "nome VARCHAR(255)", "console VARCHAR(255)"),
    cursor=mysql_cursor,
    if_not_exists=True
)

create_table(
    table="jogos",
    attributes=("id INT AUTO_INCREMENT PRIMARY KEY", "nome VARCHAR(255)", "data_lancamento DATE"),
    cursor=mysql_cursor,
    if_not_exists=True,
)

# Insert data
insert_into(
    table="usuarios",
    attributes=("nome", "console"),
    values=(
        ("Victor", "PS4"),
        ("João", "Xbox"),
        ("Maria", "PC"),
        ("José", "PS4"),
    ),
    cursor=mysql_cursor,
)

insert_into(
    table="jogos",
    attributes=("nome", "data_lancamento"),
    values=(
        ("God of War", "2018-04-20"),
        ("Uncharted 4", "2016-05-10"),
        ("The Last of Us", "2013-06-14"),
    ),
    cursor=mysql_cursor,
)

# Tests
select_from_where(
    table="usuarios",
    attributes=("id", "nome"),
    cursor=mysql_cursor,
    conditions="console = 'PS4'",
)

print(fetch_all(cursor=mysql_cursor))

delete_from_where(
    table="usuarios",
    conditions="nome = 'Victor'",
    cursor=mysql_cursor,
)

select_from_where(
    table="usuarios",
    attributes=("*",),
    cursor=mysql_cursor,
    conditions="console = 'PS4'",
)

print(fetch_all(cursor=mysql_cursor))

select_from_where(
    table="jogos",
    attributes=("*",),
    cursor=mysql_cursor,
)

print(fetch_all(cursor=mysql_cursor))

delete_from_where(
    table="jogos",
    conditions="nome = 'Uncharted 4'",
    cursor=mysql_cursor,
)

select_from_where(
    table="jogos",
    attributes=("*",),
    cursor=mysql_cursor,
)

print(fetch_all(cursor=mysql_cursor))

drop_database(database=DATABASE_NAME(), cursor=mysql_cursor)
mysql_database.close()
