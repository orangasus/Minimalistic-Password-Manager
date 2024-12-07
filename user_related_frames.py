import tkinter as tk

from standard_frame import StandardFrame


class LoginIntoAppFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.str_var_user_login = tk.StringVar()
        self.str_var_user_password = tk.StringVar()

        self.login_entry = tk.Entry(self, textvariable=self.str_var_user_login)
        self.password_entry = tk.Entry(self, textvariable=self.str_var_user_password)

        self.login_button = tk.Button(self, command=self.on_login_btn_click, text='LOGIN')
        self.create_user_button = tk.Button(self, command=self.on_create_user_btn_click, text='CREATE')

        self.fill_window_layout()

    def on_create_user_btn_click(self):
        self.controller.show_frame(self.controller.create_user_frame)

    def fill_window_layout(self):
        self.login_entry.pack()
        self.password_entry.pack()
        self.login_button.pack()
        self.create_user_button.pack()

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
                print('Wrong password')
        else:
            print('User doesn\' exist')


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
