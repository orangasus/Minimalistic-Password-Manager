import tkinter as tk
from tkinter import messagebox

import pyperclip as pclip

from standard_frame import StandardFrame


class ItemInfoFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.cred_name_sv = tk.StringVar()
        self.cred_login_sv = tk.StringVar()
        self.cred_password_sv = tk.StringVar()

        self.cred_login_head_label = tk.Label(self, text='Login')
        self.cred_password_head_label = tk.Label(self, text='Password')
        self.cred_name_head_label = tk.Label(self, text='Name')

        self.cred_name_label = tk.Label(self, textvariable=self.cred_name_sv)
        self.cred_login_label = tk.Label(self, textvariable=self.cred_login_sv)
        self.cred_password_label = tk.Label(self, textvariable=self.cred_password_sv)

        self.delete_item_button = tk.Button(self, command=self.on_delete_btn_click, text='DELETE')
        self.edit_item_button = tk.Button(self, command=self.on_edit_btn_click, text='EDIT')

        self.copy_login_button = tk.Button(self, command=self.on_copy_login_btn_click, text='COPY')
        self.copy_pswd_button = tk.Button(self, command=self.on_copy_pswd_btn_click, text='COPY')

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

    def fill_window_layout(self):
        self.cred_name_head_label.grid(row=0, column=0, columnspan=2)
        self.cred_name_label.grid(row=1, column=0, columnspan=2)
        self.cred_login_head_label.grid(row=2, column=0, columnspan=2)
        self.cred_login_label.grid(row=3, column=0, columnspan=2)
        self.copy_login_button.grid(row=3, column=2)
        self.cred_password_head_label.grid(row=4, column=0, columnspan=2)
        self.cred_password_label.grid(row=5, column=0, columnspan=2)
        self.copy_pswd_button.grid(row=5, column=2)
        self.edit_item_button.grid(row=6, column=0)
        self.delete_item_button.grid(row=6, column=2)

    def update_labels_info(self, name, login, password):
        self.cred_name_sv.set(name)
        self.cred_login_sv.set(login)
        self.cred_password_sv.set(password)


class EmptyFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.label = tk.Label(self, text='Nothing Selected')
        self.label.pack()


class UserContentFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.user_content_state = {'cur_item_ind': None}

        self.item_frame_related_container = tk.Frame(self)

        self.item_info_frame = ItemInfoFrame(self.item_frame_related_container, self)
        self.item_edit_frame = EditCredItemFrame(self.item_frame_related_container, self)
        self.item_create_frame = AddListItemFrame(self.item_frame_related_container, self)
        self.item_empty_frame = EmptyFrame(self.item_frame_related_container, self)

        self.create_item_button = tk.Button(self, command=self.on_create_item_btn_click, text='CREATE')

        self.logout_button = tk.Button(self, command=self.on_logout_btn_click, text='LOGOUT')

        self.cred_listbox_scrollbar = tk.Scrollbar(self)
        self.cred_listbox = tk.Listbox(self, bg='red', yscrollcommand=self.cred_listbox_scrollbar.set,
                                       selectmode=tk.SINGLE)
        self.cred_listbox_scrollbar.configure(command=self.cred_listbox.yview)
        self.cred_listbox.bind('<<ListboxSelect>>', self.on_items_list_click)

        self.fill_window_layout()
        self.show_item_related_frame(self.item_empty_frame)

    def on_logout_btn_click(self):
        self.controller.user_items_list = []
        self.controller.app_state['cur_user'] = None
        self.controller.show_frame(self.controller.login_form_frame)

    def show_item_related_frame(self, frame):
        frame.tkraise()

    def clear_items_listbox(self):
        self.cred_listbox.delete(0, self.cred_listbox.size() - 1)

    def on_items_list_click(self, event):
        try:
            self.user_content_state['cur_item_ind'] = self.cred_listbox.curselection()[0]
        except IndexError:
            self.user_content_state['cur_item_ind'] = None

        if self.user_content_state['cur_item_ind'] is not None:
            selected_item = self.controller.user_items_list[self.user_content_state['cur_item_ind']]
            self.item_info_frame.update_labels_info(selected_item.cred_name,
                                                    selected_item.cred_login,
                                                    selected_item.cred_pwd)
            self.show_item_related_frame(self.item_info_frame)

    def upload_items_to_listbox(self):
        self.clear_items_listbox()
        for i, cred_item in enumerate(self.controller.user_items_list):
            listbox_item_name = f'{cred_item.cred_name} - {cred_item.cred_login}'
            self.cred_listbox.insert(i, listbox_item_name)

    def fill_window_layout(self):
        self.item_frame_related_container.grid(row=0, column=2, sticky='news')
        self.cred_listbox.grid(row=0, column=0, rowspan=2)
        self.cred_listbox_scrollbar.grid(row=0, column=1, rowspan=2, sticky='ns')
        self.create_item_button.grid(row=2, column=0)
        self.logout_button.grid(row=0, column=3, sticky='ne')

        self.item_info_frame.grid(row=0, column=0, sticky='news')
        self.item_edit_frame.grid(row=0, column=0, sticky='news')
        self.item_create_frame.grid(row=0, column=0, sticky='news')
        self.item_empty_frame.grid(row=0, column=0, sticky='news')

    def on_create_item_btn_click(self):
        self.show_item_related_frame(self.item_create_frame)


class AddListItemFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.str_var_cred_login = tk.StringVar()
        self.str_var_cred_password = tk.StringVar()
        self.str_var_cred_name = tk.StringVar()

        self.cred_login_label = tk.Label(self, text='Login')
        self.cred_password_label = tk.Label(self, text='Password')
        self.cred_name_label = tk.Label(self, text='Name')

        self.cred_login_entry = tk.Entry(self, textvariable=self.str_var_cred_login)
        self.cred_password_entry = tk.Entry(self, textvariable=self.str_var_cred_password)
        self.cred_name_entry = tk.Entry(self, textvariable=self.str_var_cred_name)

        self.save_cred_button = tk.Button(self, text='SAVE', command=self.on_save_btn_click)

        self.fill_window_layout()

    def check_item_info_before_creating(self, user, name, login, password):
        for el in (name, login, password):
            if el == '':
                return False

        if not self.check_that_item_unique(user, name, login, password):
            print(user, name, login, password)
            tk.messagebox.showinfo('Error', 'Item already exists')
            return False

        return True

    def check_that_item_unique(self, user, name, login, password):
        res = self.controller.db_manager.cred_table_manager.search_for_item_match(user, name, login, password)
        print(res)
        return True if res is None else False

    def fill_window_layout(self):
        self.cred_name_label.pack()
        self.cred_name_entry.pack()
        self.cred_login_label.pack()
        self.cred_login_entry.pack()
        self.cred_password_label.pack()
        self.cred_password_entry.pack()
        self.save_cred_button.pack()

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


class EditCredItemFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.item_id = 0

        self.cred_name_sv = tk.StringVar()
        self.cred_login_sv = tk.StringVar()
        self.cred_password_sv = tk.StringVar()

        self.cred_name_entry = tk.Entry(self, textvariable=self.cred_name_sv)
        self.cred_login_entry = tk.Entry(self, textvariable=self.cred_login_sv)
        self.cred_password_entry = tk.Entry(self, textvariable=self.cred_password_sv)

        self.save_changes_button = tk.Button(self, text='SAVE', command=self.on_save_btn_click)

        self.fill_window_layout()

    def fill_window_layout(self):
        self.cred_name_entry.pack()
        self.cred_login_entry.pack()
        self.cred_password_entry.pack()
        self.save_changes_button.pack()

    def set_item_id(self, id):
        self.item_id = id

    def upload_item_vals_to_entries(self):
        item = self.controller.controller.user_items_list[self.controller.user_content_state['cur_item_ind']]
        self.cred_name_sv.set(item.cred_name)
        self.cred_login_sv.set(item.cred_login)
        self.cred_password_sv.set(item.cred_pwd)

    def on_save_btn_click(self):
        self.controller.db_manager.cred_table_manager.update_creds_item_by_id(
            self.item_id, self.cred_login_sv.get(),
            self.cred_password_sv.get(), self.cred_name_sv.get()
        )
        self.controller.controller.fill_user_items_list()
        self.controller.item_info_frame.update_labels_info(self.cred_name_sv.get(),
                                                           self.cred_login_sv.get(), self.cred_password_sv.get())
        self.controller.upload_items_to_listbox()
        self.controller.show_item_related_frame(self.controller.item_info_frame)
