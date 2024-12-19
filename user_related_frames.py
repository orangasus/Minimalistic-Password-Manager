import customtkinter as ctk

import app_styling as app_style
from entry_with_placeholder import EntryWithPlaceholder
from error_frame import ErrorFrame
from standard_frame import StandardFrame


class LoginIntoAppFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.configure(fg_color=app_style.BACKGROUND_GREY_COLOR)

        self.str_var_user_login = ctk.StringVar()
        self.str_var_user_password = ctk.StringVar()

        self.login_entry = EntryWithPlaceholder(self, self.str_var_user_login, 'Username')
        self.password_entry = EntryWithPlaceholder(self, self.str_var_user_password, 'Password')

        self.error_frame = ErrorFrame(self, 'Error', 'Wrong credentials', 3000)

        self.login_button = ctk.CTkButton(self, command=self.on_login_btn_click, text='LOGIN',
                                          width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL, fg_color=app_style.ACCENT_COLOR)
        self.create_user_button = ctk.CTkButton(self, command=self.on_create_user_btn_click, text='CREATE',
                                                width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL, fg_color=app_style.ACCENT_COLOR)

        self.setup_grid()
        self.fill_window_layout()

    def reset_frame(self):
        self.login_entry.show_placeholder()
        self.password_entry.show_placeholder()
        self.focus()

    def on_create_user_btn_click(self):
        self.controller.show_frame(self.controller.create_user_frame)
        self.reset_frame()

    def setup_grid(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(4, weight=1)
        for i in range(2):
            self.grid_columnconfigure(i, weight=1)

    def fill_window_layout(self):
        self.login_entry.grid(row=1, column=0, columnspan=2, sticky='s', pady=2)
        self.password_entry.grid(row=2, column=0, columnspan=2, sticky='n', pady=2)
        self.login_button.grid(row=3, column=0, sticky='ne', pady=10, padx=20)
        self.create_user_button.grid(row=3, column=1, sticky='nw', pady=10, padx=20)

    def on_login_btn_click(self):
        login = self.str_var_user_login.get()
        password = self.str_var_user_password.get()

        if self.db_manager.user_table_manager.check_if_user_exists(login):
            real_password = self.db_manager.user_table_manager.get_user_password(login)
            if real_password == password:
                self.controller.app_state['cur_user'] = login
                print(self.controller.app_state['cur_user'])
                self.controller.fill_user_items_list()
                self.controller.user_content_frame.upload_items_to_listbox()
                self.controller.show_frame(self.controller.user_content_frame)
                self.reset_frame()
            else:
                self.error_frame.show_error_frame()
        else:
            self.error_frame.show_error_frame()


class CreateUserFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.configure(fg_color=app_style.BACKGROUND_GREY_COLOR)

        self.str_var_user_login = ctk.StringVar()
        self.str_var_user_password = ctk.StringVar()

        self.login_entry = EntryWithPlaceholder(self, entry_str_var=self.str_var_user_login, pl_text='Login')
        self.password_entry = EntryWithPlaceholder(self, entry_str_var=self.str_var_user_password, pl_text='Password')

        self.create_button = ctk.CTkButton(self, command=self.on_create_btn_click, text='CREATE',
                                           width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,  fg_color=app_style.ACCENT_COLOR)

        self.back_button = ctk.CTkButton(self, command=self.on_back_btn_click, text='BACK',
                                           width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                           fg_color=app_style.ACCENT_COLOR)

        self.error_frame_user_exists = ErrorFrame(self, 'Error', 'User exists', 3000)
        self.error_frame_empty_entry = ErrorFrame(self, 'Error', 'Entry empty', 3000)

        self.fill_window_layout()

    def reset_frame(self):
        self.login_entry.show_placeholder()
        self.password_entry.show_placeholder()
        self.focus()

    def on_back_btn_click(self):
        self.reset_frame()
        self.controller.show_frame(self.controller.login_form_frame)

    def fill_window_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.login_entry.grid(row=1, column=0, columnspan=2, pady=2)
        self.password_entry.grid(row=2, column=0, columnspan=2, pady=2)
        self.back_button.grid(row=3, column=0, pady=10, sticky='e', padx=20)
        self.create_button.grid(row=3, column=1, pady=10, sticky='w', padx=20)

    def on_create_btn_click(self):
        login = self.str_var_user_login.get()
        password = self.str_var_user_password.get()

        if (password != '' and login != '') and (self.login_entry.touched and self.password_entry.touched):
            if not self.db_manager.user_table_manager.check_if_user_exists(login):
                self.db_manager.user_table_manager.insert_user(login, password)
                self.controller.show_frame(self.controller.login_form_frame)
            else:
                self.error_frame_user_exists.show_error_frame()
        else:
            self.error_frame_empty_entry.show_error_frame()
