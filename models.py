import re

from psycopg2 import connect, OperationalError
from psycopg2._psycopg import cursor

from hash_password import hash_password


def execute_sql(sql_code, db_name, cur_id=''):
    result = None
    try:
        cnx = connect(user='postgres', password='coderslab', host='localhost', database=db_name)
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_code)
        if cur_id is not None:
            cursor.fetchone()[cur_id]
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
        if self._id == -1:
            save_name = execute_sql(db_name='messenger_db',
                                    sql_code=f"insert into users(username, hashed_password) values ('{self.username}', '{self.hashed_password}') returning id;",
                                    cur_id=self._id)
            return True
        return False

    @staticmethod
    def load_user_by_id(id_):
        load_user_id = execute_sql(db_name='messenger_db',
                                   sql_code=f"SELECT id, username, hashed_password FROM users WHERE id={id_}")

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
    user = Users('wojtek', 'abc123')
    saveto = user.save_to_db()
    # lodad_from_id = user.load_user_by_id(8)
