import sys
import sqlite3
from htwdresden import RZLogin

DB_NAME = 'htw_bot.db'


def setup():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        try:
            c.execute('''CREATE TABLE `logins` (
                `chat_id`	TEXT NOT NULL UNIQUE,
                `login`	    TEXT NOT NULL,
                `password`	TEXT NOT NULL
            );''')
        except sqlite3.OperationalError:
            print(f'{DB_NAME} with table `logins` already exists.')


def persist_login(chat_id: str, login: RZLogin) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        try:
            c.execute('''INSERT into `logins` values (?,?,?);''', (chat_id, login.s_number, login.password))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f'Error on persisting login for `{chat_id}` `{login}`: {e}', file=sys.stderr)
            return False
        return True


def remove_login(chat_id: str) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''DELETE from `logins` WHERE chat_id = ?;''', (chat_id,))
        conn.commit()
        return c.rowcount == 1


def fetch_login_for_user(chat_id: str) -> RZLogin or None:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''SELECT * from `logins` WHERE chat_id = ?;''', (chat_id,))
        res = c.fetchone()
        if res is not None:
            return RZLogin(res[1], res[2])
        else:
            return None


def fetch_all_logins() -> [(str, RZLogin)]:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''SELECT * from `logins`;''')
        res = c.fetchall()
        return [(r[0], RZLogin(r[1], r[2])) for r in res]
