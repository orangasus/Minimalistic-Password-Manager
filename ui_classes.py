import tkinter as tk

from auto_editor.utils.types import anchor

from db_management import DataBaseManager

class AppWindow(tk.Tk):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.geometry('480x640')

        self.frame_container = tk.Frame(self, background='black')

        self.frame_container.pack(fill='both', expand=True)

        self.add_list_item_frame = AddListItemFrame(self.frame_container, self, db_manager)
        self.main_menu_frame = MainMenuFrame(self.frame_container, self, db_manager)

        self.add_list_item_frame.grid(row=0, column=0, sticky='news')
        self.main_menu_frame.grid(row=0, column=0, sticky='news')

        self.show_frame(self.main_menu_frame)

    def show_frame(self, frame):
        frame.tkraise()

class AddListItemFrame(tk.Frame):
    def __init__(self, parent, controller, db_manager):
        super().__init__(parent)
        self.controller = controller
        self.db_manager = db_manager
        self.parent = parent

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
        self.user_login_entry.pack(anchor)
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


class MainMenuFrame(tk.Frame):
    def __init__(self, parent, controller, db_manager):
        super().__init__(parent)
        self.parent = parent
        self.db_manager = db_manager
        self.controller = controller

        self.show_cred_button = tk.Button(self, text='SHOW', command=self.on_show_btn_click)
        self.create_cred_button = tk.Button(self, text='CREATE', command=self.on_create_btn_click)

        self.fill_window_layout()

    def fill_window_layout(self):
        self.show_cred_button.pack()
        self.create_cred_button.pack()

    def on_show_btn_click(self):
        items = self.db_manager.cred_table_manager.get_all_creds_items_by_user('pepe')
        print(items)

    def on_create_btn_click(self):
        self.controller.show_frame(self.controller.add_list_item_frame)

db_manager = DataBaseManager()
app = AppWindow(db_manager)
app.mainloop()
