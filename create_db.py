from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase

db_name = input("Name your database: ")
create_db = f"create database {db_name};"

create_users = """
    create table users (
    id serial,
    username varchar(255),
    hashed_password varchar(80) unique,
    primary key(id)
    );"""

create_messages = """
    create table messages (
    id serial,
    from_id int,
    to_id int,
    creation_date timestamp,
    primary key(id),
    foreign key(from_id) references users on delete cascade,
    foreign key(to_id) references  users on delete cascade
    );"""

db_user = "postgres"
db_password = "coderslab"
host = "127.0.0.1"


try:
    cnx = connect(user = db_user, password = db_password, host = host)
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(create_db)
except OperationalError as e:
    print("ERROR!", e)
except DuplicateDatabase:
    print(f"Database {db_name} already exist.")

cursor.close()
cnx.close()

