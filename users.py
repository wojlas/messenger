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

def list_users(cur):
    users = Users.load_all_users(cur)
    for user in users:
        print(user.username)

def create_user(cur, username, password):
    if len(password) < 8:
        print("Password is tho short. It should have minimum 8 characters.")
    else:
        try:
            user = Users(username=username, password=password)
            user.save_to_db()
            print("User created")
        except UniqueViolation as e:
            print("User already exist", e)

def delete_user(cur, username, password):
    user = Users.load_user_by_username(cur, username)
    if not user:
        print("User doesn't exist!")
    elif check_password(password, user.hashed_password):
        user.delete(cur)
        print("User deleted.")
    else:
        print("Incorrect password!")

def edit_user(cur, username, password, new_pass):
    user = Users.load_user_by_username(cur, username)
    if not user:
        print("User does not exist!")
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print("Password is tho short. It should have minimum 8 characters.")
        else:
            user.hashed_password = new_pass
            user.save_to_db(cur)
            print("Password changed.")
    else:
        print("Incorrect password")

if __name__=='__main__':
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
