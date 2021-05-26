from create_db import execute_sql
from hash_password import hash_password


class Users():
    def __init__(self, username, password="", salt=None):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

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
        if self._id == -1:
            execute_sql(
                sql_code=f"insert into users(username, hashed_password) values ('{self.username}','{self.hashed_password}') returning id",
                db_name='messenger_db')
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = '''UPDATE Users SET username=%s, hashed_password=%sWHERE id=%s'''
            values = (self.username, self.hashed_password, self.id)
            execute_sql(sql_code=sql,
                        db_name='messenger_db')
            return True

    @staticmethod
    def load_user_by_id(id_):
        execute_sql(sql_code=f"select id, username, hashed_password from users where id = {id_};",
                    db_name='messenger_db')
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user.username
        else:
            return None

    @staticmethod
    def load_user_by_username(username, cursor):
        execute_sql(sql_code=f"select id, username, hashed_password from users where username = {username};",
                    db_name='messenger_db')
        data = cursor.fetchone()
        if data:
            id_, username, hashed_password = data
            loaded_user = Users(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        execute_sql(sql_code='select * from users;',
                    db_name='messenger_db')
        users = []
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = Users()
            loaded_user._id = id_
            loaded_user.username = username
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete_user(self, cursor):
        execute_sql(sql_code=f'delete from users where id = {self._id}',
                    db_name='messenger_db')
        self._id = -1
        return True


class Messages:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_data = None

    @property
    def id(self):
        return self._id

    def save_to_db(self):
        if self._id == -1:
            execute_sql(
                sql_code=f"insert into messages(from_id, to_id, text) values ('{self.from_id}','{self.to_id}', '{self.text}') returning id",
                db_name='messenger_db')
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = '''UPDATE messages SET from_id=%s, to_id=%s, text=%s WHERE id=%s'''
            values = (self.from_id, self.to_id, self.text, self.id)
            execute_sql(sql_code=sql,
                        db_name='messenger_db')
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        execute_sql(sql_code='select * from messages;',
                    db_name='messenger_db')
        messages = []
        for row in cursor.fetchall():
            id_, from_id, to_id, text = row
            load_messages = Messages()
            load_messages._id = id_
            load_messages.from_id = from_id
            load_messages.to_id = to_id
            load_messages.text = text
            load_messages.creation_data = creation_data
            messages.append(load_messages)
        return messages


if __name__=='__main__':
    user = Users(username='Ola', password='test123')
    # user.save_to_db()
    # user.load_user_by_id(3)
    # user.load_all_users()
