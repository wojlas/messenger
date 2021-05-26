import re

from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

"""Program to create database (db name input by user) and tables for users and messages"""

# db_name = input("Enter name of database: ")
db_name = 'messenger_db'

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
    text varchar(255),
    primary key(id),
    foreign key(from_id) references users(id) on delete cascade,
    foreign key(to_id) references  users(id) on delete cascade
    );"""

#login data
db_user = "postgres"
db_password = "coderslab"
host = "127.0.0.1"

#create database
def execute_sql(sql_code, db_name):
    """
    Run given sql code with psycopg2.
    :param str sql_code: sql code to run
    :param str db: name of db,
    :rtype: list
    :return: data from psycobg2 cursor as a list (can be None) if nothing to fetch.
    """
    result = None
    try:
        cnx = connect(user=db_user, password=db_password, host=host, database=db_name)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_code)
        if re.match(r'(?i)select', sql_code):
            result = cursor.fetchall()
        print("Sukces")
    except OperationalError as e:
        print("Błąd!", e)
        return
    cursor.close()
    cnx.close()
    return result

def create_db():
    try:
        execute_sql(sql_code= f"create database {db_name};",
                    db_name='')
        return "Database created!"
    except DuplicateDatabase:
        return "Database already exist"
        pass


#create table users in database
def create_users_table():
    try:
        execute_sql(sql_code= create_users,
                    db_name=db_name)
        return "Table users created!"
    except DuplicateTable:
        return "Table Users already exist"

#create table messages in database
def create_messages_table():
    try:
        execute_sql(sql_code=create_messages,
                    db_name=db_name)
        return "Table Messages created!"
    except DuplicateTable:
        return "Table Messages already exist"

# print(create_db())
# print(create_users_table())
# print(create_messages_table())