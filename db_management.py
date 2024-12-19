# Classes responsible for interacting
# with app's database

import sqlite3

import encryption_module


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
        USER_PASSWORD BLOB,
        ENCRYPTION_KEY TEXT)''')

    def delete_user(self, login):
        try:
            self.cur.execute('DELETE FROM USERS WHERE USER_LOGIN = ?', (login,))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")

    def get_user_encryption_key_by_login(self, login):
        self.cur.execute('SELECT ENCRYPTION_KEY FROM USERS WHERE USER_LOGIN = ?', (login,))
        return self.cur.fetchone()[0]

    def update_user_password(self, login, new_password):
        new_hashed_password = encryption_module.hash_password(new_password)

        try:
            self.cur.execute('UPDATE USERS SET USER_PASSWORD = ? WHERE USER_LOGIN = ?', (new_hashed_password, login))
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
            return self.cur.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error retrieving password: {e}")

    def insert_user(self, login, password):
        try:
            encryption_key = encryption_module.generate_user_key()
            hashed_password = encryption_module.hash_password(password)
            self.cur.execute('INSERT INTO USERS(USER_LOGIN, USER_PASSWORD, ENCRYPTION_KEY) VALUES (?, ?, ?)',
                             (login, hashed_password, encryption_key))
            self.con.commit()
        except sqlite3.IntegrityError as e:
            print(f"Error inserting user: {e}")


class CredentialsTableManager:
    def __init__(self, connection, controller):
        self.con = connection
        self.cur = self.con.cursor()
        self.controller = controller
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
            encryption_key = self.controller.user_table_manager.get_user_encryption_key_by_login(user_login)
            encrypted_password = encryption_module.encrypt_password(cred_password, encryption_key)
            self.cur.execute(
                'INSERT INTO CREDENTIALS(USER_LOGIN, CRED_NAME, CRED_LOGIN, CRED_PASSWORD) VALUES (?, ?, ?, ?)',
                (user_login, cred_name, cred_login, encrypted_password))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error inserting credential: {e}")

    def delete_creds_item_by_id(self, item_id):
        try:
            self.cur.execute('DELETE FROM CREDENTIALS WHERE ID = ?', (item_id,))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error deleting credential: {e}")

    def search_for_item_match(self, user, cred_name, cred_login, cred_password):
        try:
            encryption_key = self.controller.user_table_manager.get_user_encryption_key_by_login(user)
            encrypted_password = encryption_module.encrypt_password(cred_password, encryption_key)
            self.cur.execute(
                'SELECT ID FROM CREDENTIALS WHERE USER_LOGIN = ? AND CRED_LOGIN = ? AND CRED_PASSWORD = ? AND CRED_NAME = ?',
                (user, cred_login, encrypted_password, cred_name))
            return self.cur.fetchone()
        except sqlite3.Error as e:
            print(f"Error searching for item match: {e}")

    def update_creds_item_by_id(self, user, item_id, cred_login, cred_password, cred_name):
        try:
            encryption_key = self.controller.user_table_manager.get_user_encryption_key_by_login(user)
            encrypted_password = encryption_module.encrypt_password(cred_password, encryption_key)
            self.cur.execute('UPDATE CREDENTIALS SET CRED_LOGIN = ?, CRED_PASSWORD = ?, CRED_NAME = ? WHERE ID = ?',
                             (cred_login, encrypted_password, cred_name, item_id))
            self.con.commit()
        except sqlite3.Error as e:
            print(f"Error updating credential: {e}")

    def get_all_creds_items_by_user(self, user_login):
        try:
            my_tuple = (user_login,)
            self.cur.execute('SELECT * FROM CREDENTIALS WHERE USER_LOGIN = ?', my_tuple)
            res = self.cur.fetchall()
            decrypted_res = []
            encryption_key = self.controller.user_table_manager.get_user_encryption_key_by_login(user_login)
            for el in res:
                el = list(el)
                el[4] = encryption_module.decrypt_password(el[4], encryption_key)
                decrypted_res.append(el)
            return decrypted_res
        except sqlite3.Error as e:
            print(f"Error retrieving credentials: {e}")

    def check_if_item_is_unique_for_user(self, user_login, cred_name,
                                         cred_login, cred_password):
        try:
            self.cur.execute(
                'SELECT ID FROM CREDENTIALS WHERE USER_LOGIN = ? AND CRED_NAME = ? AND CRED_LOGIN = ? AND CRED_PASSWORD = ?',
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
        self.cred_table_manager = CredentialsTableManager(self.con, self)
        self.user_table_manager = UserTableManager(self.con)

    def close_db_connection(self):
        self.con.close()
