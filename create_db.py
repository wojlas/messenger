from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

"""Program makes database (db name input by user) and tables for users and messages"""

db_name = input("Name your database: ")
user_table_name = 'users'
messages_table_name = 'messages'
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

#login data
db_user = "postgres"
db_password = "coderslab"
host = "127.0.0.1"

#create database
try:
    cnx = connect(user=db_user, password=db_password, host=host)
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(create_db)
except OperationalError as e:
    print("ERROR!", e)
except DuplicateDatabase:
    print(f"Database {db_name} already exist.")
    pass

#create table users in database
try:
    cnx = connect(user=db_user, password=db_password, host=host, database = db_name)
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(create_users)
except OperationalError as e:
    print("ERROR!", e)
except DuplicateTable:
    print(f"Table {user_table_name} already exist.")
    pass

#create table messages in database
try:
    cnx = connect(user=db_user, password=db_password, host=host, database = db_name)
    cnx.autocommit = True
    cursor = cnx.cursor()
    cursor.execute(create_messages)
except OperationalError as e:
    print("ERROR!", e)
except DuplicateTable:
    print(f"Table {messages_table_name} already exist.")
    pass


#end of connection
cursor.close()
cnx.close()
