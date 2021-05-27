import argparse
from models import Messages, Users
from psycopg2 import connect, OperationalError
from hash_password import check_password

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-t", "--to", help="username for whom to send the message")
parser.add_argument("-s", "--send", help="text your message",)
parser.add_argument("-l", "--list", help="list all messages", action='store_true')

args = parser.parse_args()

def print_user_messages(data, user):
    '''function print all messages for username'''
    messages = Messages.load_all_messages(data, user.id)
    for message in messages:
        from_ = Users.load_user_by_id(data, messages.from_id)
        print(10 * "-")
        print(f"from: {from_.username}")
        print(f"data: {message.creation_date}")
        print(message.text)
        print(10 * "-")

def send_message(data, from_id, recipient_name, text):
    '''function send a messages'''
    if len(text) > 255:
        print("Message is too long!")
        return
    to = Users.load_user_by_username(data, recipient_name)
    if to:
        message = Messages(from_id, to.id, text=text)
        message.save_to_db(data)
        print("Message send")
    else:
        print("User does not exists.")

...
if __name__ == '__main__':
    try:
        cnx = connect(database="messenger_db", user="postgres", password="coderslab", host="127.0.0.1")
        cnx.autocommit = True
        cursor = cnx.cursor()
        if args.username and args.password:
            user = Users.load_user_by_username(cursor, args.username)
            if check_password(args.password, user.hashed_password):
                if args.list:
                    print_user_messages(cursor, user)
                elif args.to and args.send:
                    send_message(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print("Incorrect password or User does not exists!")
        else:
            print("username and password are required")
            parser.print_help()
        cnx.close()
    except OperationalError as err:
        print("Connection Error: ", err)

