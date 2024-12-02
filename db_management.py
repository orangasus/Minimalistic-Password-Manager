import sqlite3


class UserTableManager:
    def __init__(self, connection):
        self.con = connection
        self.cur = self.con.cursor()
        self.create_user_db_if_needed()

    def create_user_db_if_needed(self):
        self.con.execute('''
        CREATE TABLE IF NOT EXISTS USERS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_LOGIN TEXT,
        USER_PASSWORD TEXT)''')

    def delete_user_in_db(self, login):
        self.cur.execute('DELETE FROM USERS WHERE USER_LOGIN = ?', (login,))
        self.con.commit()

    def update_user_password(self, login, new_password):
        self.cur.execute('UPDATE USERS SET USER_PASSWORD = ? WHERE USER_LOGIN = ?', (new_password, login))
        self.con.commit()

    def check_if_user_exists(self, login):
        self.cur.execute('SELECT ID FROM USERS WHERE USER_LOGIN = ?', (login,))
        res = self.cur.fetchall()
        return len(res) != 0

    def get_all_users(self):
        self.cur.execute('SELECT * FROM USERS')
        return self.cur.fetchall()

    def delete_user(self, login):
        self.cur.execute('DELETE FROM USERS WHERE USER_LOGIN = ?', (login,))
        self.con.commit()

    def get_user_password(self, login):
        self.cur.execute('SELECT USER_PASSWORD FROM USERS WHERE USER_LOGIN = ?', (login,))
        res = self.cur.fetchone()
        return res if res else None

class CredentialsTableManager():
    def __init__(self, connection):
        self.con = sqlite3.connect('AppDB.db')
        self.cur = self.con.cursor()
        self.create_creds_db_if_needed()

    def create_creds_db_if_needed(self):
        self.con.execute('''
        CREATE TABLE IF NOT EXISTS CREDENTIALS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_LOGIN TEXT,
        CRED_NAME TEXT,
        CRED_LOGIN TEXT,
        CRED_PASSWORD TEXT)''')

    def insert_creds_item(self):
        pass

    def delete_creds_item(self):
        pass

    def update_creds_item(self):
        pass

    def get_all_creds_items_by_user(self):
        pass

    def get_cred_item_by_cred_name(self):
        pass

    def get_cred_item_by_cred_login(self):
        pass

class DataBaseManager():
    def __init__(self):
        self.con = sqlite3.connect('AppDB.db')
        self.cred_table_manager = CredentialsTableManager(self.con)
        self.user_table_manager = UserTableManager(self.con)

    def close_db_connection(self):
        self.con.close()