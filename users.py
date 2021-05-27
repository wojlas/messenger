import argparse
from models import Users
from psycopg2 import connect, OperationalError
from psycopg2.errors import UniqueViolation
from hash_password import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")

args = parser.parse_args()

def list_users(data):
    '''function load all user from database'''
    users = Users.load_all_users(data)
    for user in users:
        print(user.username)

def create_user(data, username, password):
    '''function create new user

    password must be longer than 8 characters'''
    if len(password) < 8:
        print("Password is tho short. It should have minimum 8 characters.")
    else:
        try:
            user = Users(username=username, password=password)
            user.save_to_db()
            print("User created")
        except UniqueViolation as e:
            print("User already exist", e)

def delete_user(data, username, password):
    '''function deleted user from database'''
    user = Users.load_user_by_username(data, username)
    if not user:
        print("User doesn't exist!")
    elif check_password(password, user.hashed_password):
        user.delete(data)
        print("User deleted.")
    else:
        print("Incorrect password!")

def edit_user(data, username, password, new_pass):
    '''function edited user in database

    function checks if user in database and change his password'''
    user = Users.load_user_by_username(data, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is tho short. It should have minimum 8 characters.")
        else:
            user.hashed_password = new_pass
            user.save_to_db(data)
            print("Password changed.")
    else:
        print("Incorrect password")

if __name__=='__main__':
    #connect and communicate with database by argpars
    try:
        cnx = connect(database="messenger_db", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password and args.edit and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()
    except OperationalError as e:
        print("Connection failed", e)
