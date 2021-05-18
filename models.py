from psycopg2 import connect

from hash_password import hash_password


class Users:
    def __init__(self, username="", password=""):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password)

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password, salt=None):
        self._hashed_password = hash_password(password, salt)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def save_to_db(self):
        cnx = connect(user='postgres', password='coderslab', host='localhost', database='messenger_db')
        cnx.autocommit = True
        cursor = cnx.cursor()
        if self._id == -1:
            sql = f"insert into users(username, hashed_password) values('{self.username}', '{self.hashed_password}') returning id;"
            cursor.execute(sql)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = """UPDATE Users SET username=%s, hashed_password=%s
                                   WHERE id=%s"""
            values = (self.username, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True
        cursor.close()
        cnx.close()

    def load_user_from_id(self, id_):
        cnx = connect(user='postgres', password='coderslab', host='localhost', database='messenger_db')
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = f"select id, username, hashed_password from users where id =%s;"
        cursor.execute(sql, (id_,))
        data = cursor.fetchone()

        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return f"{id_}: {loaded_user.username}"
        else:
            return None
        cursor.close()
        cnx.close()

    @staticmethod
    def load_user_from_name(username):
        cnx = connect(user='postgres', password='coderslab', host='localhost', database='messenger_db')
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = f"select id, username, hashed_password from users where username =%s;"
        cursor.execute(sql, (username,))
        data = cursor.fetchone()

        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return f"{id_}: {loaded_user.username}"
        else:
            return None
        cursor.close()
        cnx.close()

    @staticmethod
    def load_all_users():
        cnx = connect(user='postgres', password='coderslab', host='localhost', database='messenger_db')
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = "SELECT id, username, hashed_password FROM Users"
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = Users()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user.username)
        return users

        cursor.close()
        cnx.close()

    @staticmethod
    def delete(user_id):
        cnx = connect(user='postgres', password='coderslab', host='localhost', database='messenger_db')
        cnx.autocommit = True
        cursor = cnx.cursor()
        sql = "DELETE FROM Users WHERE id=%s"
        cursor.execute(sql, (user_id,))
        return True
        cursor.close()
        cnx.close()


class Messages:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self._creation_date = None

    @property
    def id(self):
        return self._id

    @property
    def creation_date(self):
        return self._creation_date

    @staticmethod
    def load_all_message(user_id = None):
        cnx = connect(user='postgres', password='coderslab', host='localhost', database='messenger_db')
        cnx.autocommit = True
        cursor = cnx.cursor()
        if user_id:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
            cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT id, from_id, to_id, text, creation_date FROM messages"
            cursor.execute(sql)
        messages = []
        for row in cursor.fetchall():
            id_, from_id, to_id, text, creation_date = row
            loaded_message = Messages(from_id, to_id, text)
            loaded_message._id = id_
            loaded_message._creation_date = creation_date
            messages.append(loaded_message.text)
        return messages
        cursor.close()
        cnx.close()

    def save_to_db(self):
        cnx = connect(user='postgres', password='coderslab', host='localhost', database='messenger_db')
        cnx.autocommit = True
        cursor = cnx.cursor()
        if self._id == -1:
            sql = f"insert into messages(from_id, to_id, text) values('{self.from_id}', '{self.to_id}', '{self.text}') returning id, creation_date;"
            cursor.execute(sql)
            self._creation_date = cursor.fetchone()
            self._id = cursor.fetchone()
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, text=%s
                                   WHERE id=%s"""
            values = (self.self.from_id, self.to_id, self.text, self.id)
            cursor.execute(sql, values)
            return True
        cursor.close()
        cnx.close()



if __name__ == '__main__':
    user = Users(name='robert', password='abcdef')
    # saveto = user.save_to_db()
    load_from_id = user.load_user_from_id(32)
    load_from_name = user.load_user_from_name('wojtek')
    load_all = user.load_all_users()
    delete = user.delete(32)
    print(load_all)

    message = Messages(from_id=51, to_id=31, text='give me my money back!')
    # send_message = message.save_to_db()
    load_message = message.load_all_message()
    print(load_message)
