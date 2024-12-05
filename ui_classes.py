import tkinter as tk

from cred_item import CredItem
from db_management import DataBaseManager


class AppWindow(tk.Tk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.app_state = {'cur_user': None}

        self.geometry('480x640')

        self.frame_container = tk.Frame(self)

        self.frame_container.pack(fill='both', expand=True)

        self.frames_list = []

        self.add_list_item_frame = None
        self.login_form_frame = None
        self.create_user_frame = None
        self.user_content_frame = None

        self.initialize_all_frames()
        self.add_all_frames_to_grid()

        self.show_frame(self.login_form_frame)

    def initialize_all_frames(self):
        self.add_list_item_frame = AddListItemFrame(self.frame_container, self)
        self.login_form_frame = LoginIntoAppFrame(self.frame_container, self)
        self.create_user_frame = CreateUserFrame(self.frame_container, self)
        self.user_content_frame = UserContentFrame(self.frame_container, self)

        self.frames_list.extend([self.add_list_item_frame, self.login_form_frame,
                                 self.create_user_frame, self.user_content_frame])
    def add_all_frames_to_grid(self):
        for frame in self.frames_list:
            frame.grid(row=0, column=0, sticky='news')

    def show_frame(self, frame):
        frame.tkraise()


class StandardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db_manager = self.controller.db_manager


class UserContentFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.cred_items = self.get_user_cred_items(self.controller.app_state['cur_user'])

        self.create_item_button = tk.Button(self, command=self.on_create_item_btn_click, text='CREATE ITEM')

        self.fill_window_layout()

    def fill_window_layout(self):
        self.create_item_button.pack()

    def get_user_cred_items(self, user):
        res = []
        db_res = self.db_manager.cred_table_manager.get_all_creds_items_by_user(user)
        for item in db_res:
            res.append(CredItem(item))
        return res

    def on_create_item_btn_click(self):
        self.db_manager.cred_table_manager.insert_creds_item(self.controller.app_state['cur_user'], 'name', 'login',
                                                             'pswd')
        self.cred_items = self.get_user_cred_items(self.controller.app_state['cur_user'])


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
                self.controller.show_frame(self.controller.user_content_frame)
            else:
                print('Wrong password')
        else:
            print('User doesn\' exist')


class AddListItemFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.str_var_cred_login = tk.StringVar()
        self.str_var_cred_password = tk.StringVar()
        self.str_var_cred_name = tk.StringVar()
        self.str_var_user_login = tk.StringVar()

        self.cred_login_entry = tk.Entry(self, textvariable=self.str_var_cred_login)
        self.cred_password_entry = tk.Entry(self, textvariable=self.str_var_cred_password)
        self.cred_name_entry = tk.Entry(self, textvariable=self.str_var_cred_name)
        self.user_login_entry = tk.Entry(self, textvariable=self.str_var_user_login)

        self.save_cred_button = tk.Button(self, text='SAVE', command=self.on_save_btn_click)

        self.fill_window_layout()

    def fill_window_layout(self):
        self.user_login_entry.pack()
        self.cred_name_entry.pack()
        self.cred_login_entry.pack()
        self.cred_password_entry.pack()
        self.save_cred_button.pack()

    def on_save_btn_click(self):
        self.db_manager.cred_table_manager.insert_creds_item(
            self.str_var_user_login.get(), self.str_var_cred_name.get(),
            self.str_var_cred_login.get(), self.str_var_cred_password.get()
        )
        self.controller.show_frame(self.controller.main_menu_frame)


db_manager = DataBaseManager()
app = AppWindow(db_manager)
app.mainloop()
