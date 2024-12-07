import tkinter as tk

from standard_frame import StandardFrame


class ItemInfoFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.cred_name_sv = tk.StringVar()
        self.cred_login_sv = tk.StringVar()
        self.cred_password_sv = tk.StringVar()

        self.cred_name_label = tk.Label(self, textvariable=self.cred_name_sv)
        self.cred_login_label = tk.Label(self, textvariable=self.cred_login_sv)
        self.cred_password_label = tk.Label(self, textvariable=self.cred_password_sv)

        self.fill_window_layout()

    def fill_window_layout(self):
        self.cred_name_label.pack()
        self.cred_login_label.pack()
        self.cred_password_label.pack()

    def update_labels_info(self, name, login, password):
        self.cred_name_sv.set(name)
        self.cred_login_sv.set(login)
        self.cred_password_sv.set(password)


class UserContentFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.user_content_state = {'cur_item_ind': None}

        self.item_info_frame = ItemInfoFrame(self, self)

        self.create_item_button = tk.Button(self, command=self.on_create_item_btn_click, text='CREATE')
        self.delete_item_button = tk.Button(self, command=self.on_delete_btn_click, text='DELETE')
        self.edit_item_button = tk.Button(self, text='EDIT')

        self.cred_listbox_scrollbar = tk.Scrollbar(self)
        self.cred_listbox = tk.Listbox(self, bg='red', yscrollcommand=self.cred_listbox_scrollbar.set,
                                       selectmode=tk.SINGLE)
        self.cred_listbox_scrollbar.configure(command=self.cred_listbox.yview)
        self.cred_listbox.bind('<<ListboxSelect>>', self.on_items_list_click)

        self.fill_window_layout()

    def clear_items_listbox(self):
        self.cred_listbox.delete(0, self.cred_listbox.size() - 1)

    def on_items_list_click(self, event):
        self.user_content_state['cur_item_ind'] = self.cred_listbox.curselection()[0]
        selected_item = self.controller.user_items_list[self.user_content_state['cur_item_ind']]
        self.item_info_frame.update_labels_info(selected_item.cred_name,
                                                selected_item.cred_login,
                                                selected_item.cred_pwd)

    def on_delete_btn_click(self):
        item_id = self.controller.user_items_list[self.user_content_state['cur_item_ind']].db_id
        self.controller.db_manager.cred_table_manager.delete_creds_item_by_id(item_id)
        self.controller.fill_user_items_list()
        self.clear_items_listbox()
        self.upload_items_to_listbox()

    def on_edit_btn_click(self):
        item_id = self.controller.user_items_list[self.user_content_state['cur_item_ind']].db_id
        # ...

    def upload_items_to_listbox(self):
        self.clear_items_listbox()
        for i, cred_item in enumerate(self.controller.user_items_list):
            listbox_item_name = f'{cred_item.cred_name} - {cred_item.cred_login}'
            self.cred_listbox.insert(i, listbox_item_name)

    def fill_window_layout(self):
        self.item_info_frame.grid(row=0, column=2, columnspan=3, sticky='news')
        self.cred_listbox.grid(row=0, column=0, rowspan=2)
        self.cred_listbox_scrollbar.grid(row=0, column=1, rowspan=2, sticky='ns')
        self.create_item_button.grid(row=1, column=2)
        self.delete_item_button.grid(row=1, column=3)
        self.edit_item_button.grid(row=1, column=4)

    def initialize_frame_grid(self):
        pass

    def on_create_item_btn_click(self):
        self.controller.show_frame(self.controller.add_list_item_frame)


class AddListItemFrame(StandardFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.str_var_cred_login = tk.StringVar()
        self.str_var_cred_password = tk.StringVar()
        self.str_var_cred_name = tk.StringVar()

        self.cred_login_entry = tk.Entry(self, textvariable=self.str_var_cred_login)
        self.cred_password_entry = tk.Entry(self, textvariable=self.str_var_cred_password)
        self.cred_name_entry = tk.Entry(self, textvariable=self.str_var_cred_name)

        self.save_cred_button = tk.Button(self, text='SAVE', command=self.on_save_btn_click)

        self.fill_window_layout()

    def fill_window_layout(self):
        self.cred_name_entry.pack()
        self.cred_login_entry.pack()
        self.cred_password_entry.pack()
        self.save_cred_button.pack()

    def on_save_btn_click(self):
        self.db_manager.cred_table_manager.insert_creds_item(
            self.controller.app_state['cur_user'], self.str_var_cred_name.get(),
            self.str_var_cred_login.get(), self.str_var_cred_password.get()
        )
        self.controller.fill_user_items_list()
        self.controller.user_content_frame.upload_items_to_listbox()
        self.controller.show_frame(self.controller.user_content_frame)
