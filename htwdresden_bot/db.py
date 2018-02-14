import sys
import sqlite3
from htwdresden import RZLogin

DB_NAME = 'htw_bot.db'


def setup():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        try:
            c.execute('''CREATE TABLE `logins` (
                `chat_id`	  TEXT NOT NULL UNIQUE,
                `login`	      TEXT NOT NULL,
                `password`	  TEXT NOT NULL,
                `grade_count` INTEGER NOT NULL
            );''')
        except sqlite3.OperationalError:
            # db with table logins already exists
            pass
        except Exception as e:
            print(e)
            sys.exit(1)


def persist_login(chat_id: str, login: RZLogin) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        try:
            c.execute('''INSERT into `logins` values (?,?,?,?);''', (chat_id, login.s_number, login.password, -1))
            conn.commit()
        except sqlite3.IntegrityError as e:
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
        c.execute('''SELECT login, password from `logins` WHERE chat_id = ?;''', (chat_id,))
        res = c.fetchone()
        fetch_all_logins()
        if res is not None:
            return RZLogin(res[0], res[1])
        else:
            return None


def fetch_all_logins() -> [(str, int, RZLogin)]:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''SELECT chat_id, grade_count, login, password from `logins`;''')
        res = c.fetchall()
        return [(r[0], r[1], RZLogin(r[2], r[3])) for r in res]


def update_grade_count_for_user(s_number: str, new_count: int) -> bool:
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''UPDATE `logins` SET grade_count = ? WHERE login = ?;''', (new_count, s_number))
        conn.commit()
        return c.rowcount > 0
