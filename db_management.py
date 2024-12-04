import sqlite3

# TODO:
#   Add checker for values item uniqueness

class UserTableManager:
    def __init__(self, connection):
        self.con = connection
        self.cur = self.con.cursor()
        self.create_user_db_if_needed()

    def create_user_db_if_needed(self):
        self.con.execute('''
        CREATE TABLE IF NOT EXISTS USERS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_LOGIN TEXT UNIQUE,
        USER_PASSWORD TEXT)''')

    def delete_user(self, login):
        try:
            self.cur.execute('DELETE FROM USERS WHERE USER_LOGIN = ?', (login,))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")

    def update_user_password(self, login, new_password):
        try:
            self.cur.execute('UPDATE USERS SET USER_PASSWORD = ? WHERE USER_LOGIN = ?', (new_password, login))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error updating password: {e}")

    def check_if_user_exists(self, login):
        try:
            self.cur.execute('SELECT ID FROM USERS WHERE USER_LOGIN = ?', (login,))
            return self.cur.fetchone() is not None
        except sqlite3.Error as e:
            print(f"Error checking user existence: {e}")

    def get_all_users(self):
        try:
            self.cur.execute('SELECT * FROM USERS')
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving users: {e}")

    def get_user_password(self, login):
        try:
            self.cur.execute('SELECT USER_PASSWORD FROM USERS WHERE USER_LOGIN = ?', (login,))
            return self.cur.fetchone()
        except sqlite3.Error as e:
            print(f"Error retrieving password: {e}")

    def insert_user(self, login, password):
        try:
            self.cur.execute('INSERT INTO USERS(USER_LOGIN, USER_PASSWORD) VALUES (?, ?)', (login, password))
            self.con.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error inserting user: {e}")


class CredentialsTableManager:
    def __init__(self, connection):
        self.con = connection
        self.cur = self.con.cursor()
        self.create_creds_db_if_needed()

    def create_creds_db_if_needed(self):
        self.con.execute('''
        CREATE TABLE IF NOT EXISTS CREDENTIALS(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_LOGIN TEXT,
        CRED_NAME TEXT,
        CRED_LOGIN TEXT,
        CRED_PASSWORD TEXT,
        FOREIGN KEY (USER_LOGIN) REFERENCES USERS(USER_LOGIN))''')

    def insert_creds_item(self, user_login, cred_name, cred_login, cred_password):
        try:
            self.cur.execute(
                'INSERT INTO CREDENTIALS(USER_LOGIN, CRED_NAME, CRED_LOGIN, CRED_PASSWORD) VALUES (?, ?, ?, ?)',
                (user_login, cred_name, cred_login, cred_password))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error inserting credential: {e}")

    def delete_creds_item_by_id(self, item_id):
        try:
            self.cur.execute('DELETE FROM CREDENTIALS WHERE ID = ?', (item_id,))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error deleting credential: {e}")

    def update_creds_item_by_id(self, item_id, cred_login, cred_password, cred_name):
        try:
            self.cur.execute('UPDATE CREDENTIALS SET CRED_LOGIN = ?, CRED_PASSWORD = ?, CRED_NAME = ? WHERE ID = ?',
                             (cred_login, cred_password, cred_name, item_id))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error updating credential: {e}")

    def get_all_creds_items_by_user(self, user_login):
        try:
            self.cur.execute('SELECT * FROM CREDENTIALS WHERE USER_LOGIN = ?', (user_login,))
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving credentials: {e}")

    def get_cred_item_by_cred_name(self, user_login, cred_name):
        try:
            self.cur.execute('SELECT * FROM CREDENTIALS WHERE CRED_NAME = ? AND USER_LOGIN = ?',
                             (cred_name, user_login))
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving credential: {e}")

    def get_cred_item_by_cred_login(self, user_login, cred_login):
        try:
            self.cur.execute('SELECT * FROM CREDENTIALS WHERE CRED_LOGIN = ? AND USER_LOGIN = ?',
                             (cred_login, user_login))
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving credential: {e}")

    def check_if_item_is_unique_for_user(self, user_login, cred_name,
                                         cred_login, cred_password):
        try:
            self.cur.execute('SELECT ID FROM CREDENTIALS WHERE USER_LOGIN = ? AND CRED_NAME = ? AND CRED_LOGIN = ? AND CRED_PASSWORD = ?',
                             (user_login, cred_name, cred_login, cred_password))
            res = self.cur.fetchall()
            if len(res) != 0:
                return False
            return True
        except sqlite3.Error as e:
            print(f"Error checking uniqueness: {e}")



class DataBaseManager:
    def __init__(self):
        self.con = sqlite3.connect('AppDB.db')
        self.cred_table_manager = CredentialsTableManager(self.con)
        self.user_table_manager = UserTableManager(self.con)

    def close_db_connection(self):
        self.con.close()