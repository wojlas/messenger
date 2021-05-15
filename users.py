import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-l", "--list", help="list users", action="store_true")
parser.add_argument("-n", "--new_pass", help="new password")
parser.add_argument("-d", "--delete", help="delete user")
parser.add_argument("-e", "--edit", help="edit user")
args = parser.parse_args()

if args.username == True and args.password == True:
    print('user created')
    # def create_user():
    #     active_users = "select username from users;"
    #     if args.username in active_users:
    #         return "This username already exist"
    #     else:
    #         if len(args.password) < 8:
    #             sql = "insert into users (username, hashed_sword) values (%s, %s)"
    #             values = (args.username, args.password)
    #             print("User created")
    #         else: return "Password too short"

# elif args.edit == True:
#     def edit_user():
