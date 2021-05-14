from psycopg2 import connect, OperationalError

from hash_password import hash_password


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


    def save_to_db(self, cursor):
        try:
            if self._id == -1:
                cnx = connect(user=self.username, password=hash_password, host="127.0.0.1", database='messenger_db')
                cnx.autocommit = True
                cursor = cnx.cursor()
                sql = """INSERT INTO users(username, hashed_password) VALUES(%s, %s) RETURNING id"""
                values = (self.username, self.hashed_password)
                cursor.execute(sql, values)
                self._id = cursor.fetchone()[0]
                return True
            return False
        except OperationalError as e:
            print("Error", e)

    @staticmethod
    def load_user_by_id(cursor, id_):
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


if __name__ == '__main__':
    usr = Users()
    usr.username = 'wojtek'
    usr.password = 'abcdefgh'
    usr.save_to_db()
