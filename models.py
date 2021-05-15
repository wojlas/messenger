from psycopg2 import connect, OperationalError
import re
from hash_password import hash_password

def execute_sql(sql_code, db_name):
    try:
        cnx = connect(user='postgres', password='coderslab', host='127.0.0.1', database=db_name)
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

class Users:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=""):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password = password

    def save_to_db(self):
        try:
            if self._id == -1:
                save_to_db = execute_sql(db_name='messenger_db',
                                         sql_code='insert into users(username, hashed_password) values ({self.username}, {self.hashed_password}) returning id')
                self._id = cursor.fetchone()[0]
                return True
            else:
                sql = """UPDATE Users SET username=%s, hashed_password=%s WHERE id=%s"""
                values = (self.username, self.hashed_password, self.id)
                cursor.execute(sql, values)
                return True
        except OperationalError as e:
            print("Error", e)

    @staticmethod
    def load_user_by_id( id_):
        sql = "SELECT id, username, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None
#
#     @staticmethod
#     def load_all_users(cursor):
#         sql = "SELECT id, username, hashed_password FROM users"
#         users = []
#         cursor.execute(sql)
#         for row in cursor.fetchall():
#             id_, username, hashed_password = row
#             loaded_user = Users()
#             loaded_user._id = id_
#             loaded_user.username = username
#             loaded_user._hashed_password = hashed_password
#             users.append(loaded_user)
#         return users
#
#     def delete(self, cursor):
#         if id != -1:
#             sql = "DELETE FROM Users WHERE id=%s"
#             cursor.execute(sql, (self.id,))
#             self._id = -1
#             return True
#         else: pass
#
# class Messages:
#     def __init__(self, from_id, to_id, text):
#         self_id = -1
#         self.from_id = from_id
#         self.to_id = to_id
#         self.text = text
#         self.creation_data = None
#
#     @property
#     def id(self):
#         return self._id
#
#     def save_to_db(self, cursor):
#         try:
#             if self._id == -1:
#                 cnx = connect(user='postgres', password='coderslab', host="127.0.0.1", database='messenger_db')
#                 cnx.autocommit = True
#                 cursor = cnx.cursor()
#                 sql = """INSERT INTO messages(from_id, to_id, creation_date) VALUES(%s, %s, %s) RETURNING id"""
#                 values = (self.from_id, self.to_id, self.creation_data)
#                 cursor.execute(sql, values)
#                 self._id = cursor.fetchone()[0]
#                 return True
#             else:
#                 sql = """UPDATE messages SET from_id=%s, to_id=%s, creation_data=%s WHERE id=%s"""
#                 values = (self.from_id, self.to_id, self.creation_data, self.id)
#                 cursor.execute(sql, values)
#                 return True
#         # except OperationalError as e:
#         #     print("Error", e)
#
#     @staticmethod
#     def load_all_messages(cursor):
#         sql = "SELECT from_id, to_id, creation_date from messages"
#         messages = []
#         cursor.execute(sql)
#         for row in cursor.fetchall():
#             id_, from_id, to_id, creation_date = row
#             loaded_message = Messages()
#             loaded_message._id = id_
#             loaded_message.from_id = from_id
#             loaded_message.to_id = to_id
#             loaded_message.creation_data = creation_data
#             messages.append(loaded_message)
#         return messages


if __name__ == '__main__':
    usr = Users()
    usr.username = 'postgres'
    usr.password = 'test1'
    #usr.save_to_db()
    usr.load_user_by_id(2)
