import sqlite3
import calendar
import time
from utils.passwords import hash


class Users:
    def __init__(self, userid: int, username: str, password: str = '', token: str = '', api_key: str = '',
                 create_at: int = 0, id: int = 0):
        self.userid = userid
        self.username = username
        self.password = password
        self.token = token
        self.api_key = api_key
        self.create_at = create_at

        ts = calendar.timegm(time.gmtime())
        if self.create_at == 0:
            self.create_at = ts

        self.__conn = sqlite3.connect('database.db')
        self.__cursor = self.__conn.cursor()

    # 将对象插入到数据库中
    def create(self):
        docs = self.get_by_username(self.username)
        if docs is not None:
            return self
        print('username', self.username)
        if self.password == '':
            print("password is empty")
            return None
        self.password = hash(self.password)
        self.__cursor.execute(
            'INSERT INTO users (userid,username,password,token,api_key, create_at) VALUES (?, ?, ?, ?, ?, ?)',
            (self.userid, self.username, self.password, self.token, self.api_key, self.create_at))
        self.__conn.commit()
        return self

    # 从数据库中删除对象
    def delete(self):
        self.__cursor.execute('DELETE FROM users WHERE username = ?', (self.username,))
        self.__conn.commit()

    #
    def update(self, password='', token='', api_key=''):
        """
        更新对象在数据库中的信息，只能更新这三个
        """
        db_info = self.get_by_username(self.username)
        if db_info is None:
            return
        self.password = password or db_info["password"]
        self.token = token or db_info["token"]
        self.api_key = api_key or db_info["api_key"]
        self.__cursor.execute('UPDATE users SET password = ?, token = ?, api_key = ? WHERE username = ?',
                              (self.password, self.token, self.api_key, self.username))
        self.__conn.commit()

    # 从数据库中获取所有对象
    @staticmethod
    def get_all():
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('SELECT id,userid,username,password,token,api_key FROM users')
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {"id": row[0], "userid": row[1], "username": row[2], "password": row[3], "token": row[4], "api_key": row[5]}
            for row in rows]

    # 从数据库中获取指定doc_id的对象
    @staticmethod
    def get_by_username(username):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('SELECT id,userid,username,password,token,api_key FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row is not None:
            return {"id": row[0], "userid": row[1], "username": row[2], "password": row[3], "token": row[4],
                    "api_key": row[5]}
        else:
            return None

    @staticmethod
    def del_by_username(username):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM users WHERE username = ?', (username,))
        cur.close()
        conn.commit()
        conn.close()

    def __str__(self):
        return f"User(userid={self.userid}, username='{self.username}', password='{self.password}', token='{self.token}', api_key={self.api_key}, create_at={self.create_at}"


def get_by_token(token):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT id,userid,username,password,token,api_key,create_at FROM users WHERE token = ?', (token,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is not None:
        return {"id": row[0], "userid": row[1], "username": row[2], "password": row[3], "token": row[4],
                "api_key": row[5], "create_at": row[6]}
    else:
        return None


def token2user(token):
    info = get_by_token(token)
    if info is None:
        return info
    return Users(**info)
