# This is a file with frames that are responsible
# for displaying and modifying user's stored credentials

import customtkinter as ctk
import pyperclip as pclip

import app_styling as app_style
from ctk_list_view import CtkListView
from ctk_list_view_item import CtkListViewItem
from standard_frame import StandardFrame


class ItemInfoFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.configure(fg_color='white')

        self.cred_name_sv = ctk.StringVar()
        self.cred_login_sv = ctk.StringVar()
        self.cred_password_sv = ctk.StringVar()

        label_width = 150

        self.cred_login_head_label = ctk.CTkLabel(self, text='Login', font=app_style.FONT_PRESET_SMALL)
        self.cred_password_head_label = ctk.CTkLabel(self, text='Password', font=app_style.FONT_PRESET_SMALL)
        self.cred_name_head_label = ctk.CTkLabel(self, text='Name', font=app_style.FONT_PRESET_SMALL)

        self.cred_name_label = ctk.CTkLabel(self, textvariable=self.cred_name_sv, font=app_style.FONT_PRESET_MAIN,
                                            width=label_width, anchor='w', justify='left')
        self.cred_login_label = ctk.CTkLabel(self, textvariable=self.cred_login_sv, font=app_style.FONT_PRESET_MAIN,
                                             width=label_width, anchor='w', justify='left')
        self.cred_password_label = ctk.CTkLabel(self, textvariable=self.cred_password_sv,
                                                font=app_style.FONT_PRESET_MAIN, width=label_width, anchor='w',
                                                justify='left')

        self.delete_item_button = ctk.CTkButton(self, command=self.on_delete_btn_click, text='DELETE',
                                                width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                                fg_color=app_style.ACCENT_COLOR)
        self.edit_item_button = ctk.CTkButton(self, command=self.on_edit_btn_click, text='EDIT',
                                              width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                              fg_color=app_style.ACCENT_COLOR)

        self.copy_login_button = ctk.CTkButton(self, command=self.on_copy_login_btn_click, text='COPY',
                                               width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                               fg_color=app_style.ACCENT_COLOR)
        self.copy_pswd_button = ctk.CTkButton(self, command=self.on_copy_pswd_btn_click, text='COPY',
                                              width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                              fg_color=app_style.ACCENT_COLOR)

        self.fill_window_layout()

    def on_copy_pswd_btn_click(self):
        pclip.copy(self.cred_password_sv.get())

    def on_copy_login_btn_click(self):
        pclip.copy(self.cred_login_sv.get())

    def on_edit_btn_click(self):
        item_id = self.controller.controller.user_items_list[self.controller.user_content_state['cur_item_ind']].db_id
        self.controller.item_edit_frame.set_item_id(item_id)
        self.controller.item_edit_frame.upload_item_vals_to_entries()
        self.controller.show_item_related_frame(self.controller.item_edit_frame)

    def on_delete_btn_click(self):
        item_id = self.controller.controller.user_items_list[self.controller.user_content_state['cur_item_ind']].db_id
        self.controller.db_manager.cred_table_manager.delete_creds_item_by_id(item_id)
        self.controller.controller.fill_user_items_list()
        self.controller.clear_items_listbox()
        self.controller.upload_items_to_listbox()
        self.controller.show_item_related_frame(self.controller.item_empty_frame)

    def config_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def fill_window_layout(self):
        self.cred_name_head_label.grid(row=0, column=0, sticky='w', padx=10)
        self.cred_name_label.grid(row=1, column=0, sticky='w', padx=10)
        self.cred_login_head_label.grid(row=2, column=0, sticky='w', padx=10)
        self.cred_login_label.grid(row=3, column=0, sticky='w', padx=10)
        self.copy_login_button.grid(row=3, column=1, sticky='e')
        self.cred_password_head_label.grid(row=4, column=0, sticky='w', padx=10)
        self.cred_password_label.grid(row=5, column=0, sticky='w', padx=10)
        self.copy_pswd_button.grid(row=5, column=1, sticky='e')
        self.edit_item_button.grid(row=6, column=0, pady=5)
        self.delete_item_button.grid(row=6, column=1, sticky='e')

    def update_labels_info(self, name, login, password):
        self.cred_name_sv.set(name)
        self.cred_login_sv.set(login)
        self.cred_password_sv.set(password)


class EmptyFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.label = ctk.CTkLabel(self, text='Nothing Selected', font=app_style.FONT_PRESET_MAIN)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label.grid(row=0, column=0, sticky='news', padx=10, pady=10)


class UserContentFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.user_content_state = {'cur_item_ind': None}

        self.configure(fg_color=app_style.BACKGROUND_GREY_COLOR)

        self.item_frame_related_container = ctk.CTkFrame(self, fg_color='transparent')

        self.item_info_frame = ItemInfoFrame(self.item_frame_related_container, self)
        self.item_edit_frame = EditCredItemFrame(self.item_frame_related_container, self)
        self.item_create_frame = AddListItemFrame(self.item_frame_related_container, self)
        self.item_empty_frame = EmptyFrame(self.item_frame_related_container, self)

        self.create_item_button = ctk.CTkButton(self, command=self.on_create_item_btn_click, text='CREATE',
                                                width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                                fg_color=app_style.ACCENT_COLOR)

        self.logout_button = ctk.CTkButton(self, command=self.on_logout_btn_click, text='LOGOUT',
                                           width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                           fg_color=app_style.ACCENT_COLOR)

        self.cred_item_list_frame = []
        self.fill_list_item_frames()
        self.cred_listbox = CtkListView(self, self.cred_item_list_frame)

        self.fill_window_layout()
        self.show_item_related_frame(self.item_empty_frame)

    def fill_list_item_frames(self):
        i = len(self.cred_item_list_frame)
        for j in range(i):
            self.cred_item_list_frame.pop()
        for j, el in enumerate(self.controller.user_items_list):
            self.cred_item_list_frame.append(CtkListViewItem(self.cred_listbox, self, el, j))

    def on_logout_btn_click(self):
        self.controller.user_items_list = []
        self.controller.app_state['cur_user'] = None
        self.clear_items_listbox()
        self.show_item_related_frame(self.item_empty_frame)
        self.controller.show_frame(self.controller.login_form_frame)

    def show_item_related_frame(self, frame):
        frame.tkraise()

    def clear_items_listbox(self):
        self.cred_listbox.delete_all_items_from_list_view()

    def upload_items_to_listbox(self):
        self.cred_listbox.delete_all_items_from_list_view()
        self.fill_list_item_frames()
        self.cred_listbox.upload_all_items_to_list_view()

    def fill_window_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=1)

        self.item_frame_related_container.grid_columnconfigure(0, weight=1)
        self.item_frame_related_container.grid_rowconfigure(0, weight=1)

        self.item_frame_related_container.grid(row=0, column=1, sticky='news', padx=10, pady=10)
        self.cred_listbox.grid(row=0, column=0, rowspan=2, sticky='news', padx=10, pady=10)
        self.create_item_button.grid(row=2, column=0, pady=10, sticky='n')
        self.logout_button.grid(row=0, column=3, sticky='n', padx=10, pady=10)

        self.item_info_frame.grid(row=0, column=0, sticky='news')
        self.item_edit_frame.grid(row=0, column=0, sticky='news')
        self.item_create_frame.grid(row=0, column=0, sticky='news')
        self.item_empty_frame.grid(row=0, column=0, sticky='news')

    def on_create_item_btn_click(self):
        self.show_item_related_frame(self.item_create_frame)


class AddListItemFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.str_var_cred_login = ctk.StringVar()
        self.str_var_cred_password = ctk.StringVar()
        self.str_var_cred_name = ctk.StringVar()

        label_width = 150

        self.cred_login_label = ctk.CTkLabel(self, text='Login', font=app_style.FONT_PRESET_SMALL, width=label_width,
                                             justify='left', anchor='w')
        self.cred_password_label = ctk.CTkLabel(self, text='Password', font=app_style.FONT_PRESET_SMALL,
                                                width=label_width, justify='left', anchor='w')
        self.cred_name_label = ctk.CTkLabel(self, text='Name', font=app_style.FONT_PRESET_SMALL, width=label_width,
                                            justify='left', anchor='w')

        self.cred_login_entry = ctk.CTkEntry(self, textvariable=self.str_var_cred_login,
                                             font=app_style.FONT_PRESET_MAIN)
        self.cred_password_entry = ctk.CTkEntry(self, textvariable=self.str_var_cred_password,
                                                font=app_style.FONT_PRESET_MAIN)
        self.cred_name_entry = ctk.CTkEntry(self, textvariable=self.str_var_cred_name, font=app_style.FONT_PRESET_MAIN)

        self.save_cred_button = ctk.CTkButton(self, text='SAVE', command=self.on_save_btn_click,
                                              width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                              fg_color=app_style.ACCENT_COLOR)

        self.fill_window_layout()

    def check_item_info_before_creating(self, user, name, login, password):
        for el in (name, login, password):
            if el == '':
                return False

        if not self.check_that_item_unique(user, name, login, password):
            print(user, name, login, password)
            return False

        return True

    def check_that_item_unique(self, user, name, login, password):
        res = self.controller.db_manager.cred_table_manager.search_for_item_match(user, name, login, password)
        return True if res is None else False

    def fill_window_layout(self):
        self.cred_name_label.pack()
        self.cred_name_entry.pack()
        self.cred_login_label.pack()
        self.cred_login_entry.pack()
        self.cred_password_label.pack()
        self.cred_password_entry.pack()
        self.save_cred_button.pack(pady=10)

    def reset_frame(self):
        self.str_var_cred_login.set('')
        self.str_var_cred_password.set('')
        self.str_var_cred_name.set('')

    def on_save_btn_click(self):
        user = self.controller.controller.app_state['cur_user']
        name, login = self.str_var_cred_name.get(), self.str_var_cred_login.get()
        pswd = self.str_var_cred_password.get()

        if self.check_item_info_before_creating(user, name, login, pswd):
            self.controller.controller.db_manager.cred_table_manager.insert_creds_item(
                user, name, login, pswd
            )
            self.controller.controller.fill_user_items_list()
            self.controller.controller.user_content_frame.upload_items_to_listbox()
            self.controller.show_item_related_frame(self.controller.item_empty_frame)
            self.reset_frame()


class EditCredItemFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.item_id = 0

        self.cred_name_sv = ctk.StringVar()
        self.cred_login_sv = ctk.StringVar()
        self.cred_password_sv = ctk.StringVar()

        self.cred_name_entry = ctk.CTkEntry(self, textvariable=self.cred_name_sv, font=app_style.FONT_PRESET_MAIN,
                                            border_color=app_style.ACCENT_COLOR, border_width=1)
        self.cred_login_entry = ctk.CTkEntry(self, textvariable=self.cred_login_sv, font=app_style.FONT_PRESET_MAIN,
                                             border_color=app_style.ACCENT_COLOR, border_width=1)
        self.cred_password_entry = ctk.CTkEntry(self, textvariable=self.cred_password_sv,
                                                font=app_style.FONT_PRESET_MAIN, border_color=app_style.ACCENT_COLOR,
                                                border_width=1)

        self.save_changes_button = ctk.CTkButton(self, text='SAVE', command=self.on_save_btn_click,
                                                 width=app_style.BUTTON_WIDTH, font=app_style.FONT_PRESET_SMALL,
                                                 fg_color=app_style.ACCENT_COLOR)

        self.fill_window_layout()

    def fill_window_layout(self):
        self.cred_name_entry.pack(pady=5)
        self.cred_login_entry.pack(pady=5)
        self.cred_password_entry.pack(pady=5)
        self.save_changes_button.pack(pady=15)

    def set_item_id(self, id):
        self.item_id = id

    def upload_item_vals_to_entries(self):
        print(self.controller.controller.user_items_list)
        item = self.controller.controller.user_items_list[self.controller.user_content_state['cur_item_ind']]
        self.cred_name_sv.set(item.cred_name)
        self.cred_login_sv.set(item.cred_login)
        self.cred_password_sv.set(item.cred_pwd)

    def on_save_btn_click(self):
        self.controller.db_manager.cred_table_manager.update_creds_item_by_id(
            self.controller.controller.app_state['cur_user'], self.item_id, self.cred_login_sv.get(),
            self.cred_password_sv.get(), self.cred_name_sv.get()
        )
        self.controller.controller.fill_user_items_list()
        self.controller.item_info_frame.update_labels_info(self.cred_name_sv.get(),
                                                           self.cred_login_sv.get(), self.cred_password_sv.get())
        self.controller.upload_items_to_listbox()
        self.controller.show_item_related_frame(self.controller.item_info_frame)
