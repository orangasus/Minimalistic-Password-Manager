import tkinter as tk

from standard_frame import StandardFrame
from entry_with_placeholder import EntryWithPlaceholder
from error_frame import ErrorFrame


class LoginIntoAppFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.str_var_user_login = tk.StringVar()
        self.str_var_user_password = tk.StringVar()

        self.login_entry = EntryWithPlaceholder(self, self.str_var_user_login, 'Username')
        self.password_entry = EntryWithPlaceholder(self, self.str_var_user_password, 'Password')

        self.error_frame = ErrorFrame(self, self, 'Error', 'Wrong credentials', 5000)

        self.login_button = tk.Button(self, command=self.on_login_btn_click, text='LOGIN')
        self.create_user_button = tk.Button(self, command=self.on_create_user_btn_click, text='CREATE')

        self.fill_window_layout()

    def on_create_user_btn_click(self):
        self.controller.show_frame(self.controller.create_user_frame)

    def fill_window_layout(self):
        self.login_entry.grid(row=0, column=0, columnspan=2)
        self.password_entry.grid(row=1, column=0, columnspan=2)
        self.login_button.grid(row=2, column=0)
        self.create_user_button.grid(row=2, column=1)

    def on_login_btn_click(self):
        login = self.str_var_user_login.get()
        password = self.str_var_user_password.get()

        if self.db_manager.user_table_manager.check_if_user_exists(login):
            real_password = self.db_manager.user_table_manager.get_user_password(login)
            if real_password == password:
                self.controller.app_state['cur_user'] = login
                self.controller.fill_user_items_list()
                self.controller.user_content_frame.upload_items_to_listbox()
                self.controller.show_frame(self.controller.user_content_frame)
            else:
                self.error_frame.show_error_frame()
        else:
            self.error_frame.show_error_frame()


class CreateUserFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.str_var_user_login = tk.StringVar()
        self.str_var_user_password = tk.StringVar()

        self.login_entry = tk.Entry(self, textvariable=self.str_var_user_login)
        self.password_entry = tk.Entry(self, textvariable=self.str_var_user_password)

        self.create_button = tk.Button(self, command=self.on_create_btn_click, text='CREATE')

        self.fill_window_layout()

    def fill_window_layout(self):
        self.login_entry.pack()
        self.password_entry.pack()
        self.create_button.pack()

    def on_create_btn_click(self):
        login = self.str_var_user_login.get()
        password = self.str_var_user_password.get()

        self.db_manager.user_table_manager.insert_user(login, password)
        self.controller.show_frame(self.controller.login_form_frame)
