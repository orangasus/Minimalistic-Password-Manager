import customtkinter as ctk


class CtkListViewItem(ctk.CTkFrame):
    def __init__(self, parent, controller, cred_item_obj):
        super().__init__(parent)
        self.cred_item_obj = cred_item_obj
        self.controller = controller

        self.cred_name_label = ctk.CTkLabel(self, text=cred_item_obj.cred_name)
        self.cred_login_label = ctk.CTkLabel(self, text=cred_item_obj.cred_login)

        self.bind('<Button-1>', self.on_click)
        self.cred_name_label.bind('<Button-1>', self.on_click)
        self.cred_login_label.bind('<Button-1>', self.on_click)

        self.configure(border_color='black', border_width=1)

        self.fill_grid_layout()

    def fill_grid_layout(self):
        self.cred_name_label.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        self.cred_login_label.grid(row=0, column=1, padx=5, pady=5, sticky='we')

    def on_click(self, event):
        selected_item = self.cred_item_obj
        self.controller.item_info_frame.update_labels_info(selected_item.cred_name,
                                                selected_item.cred_login,
                                                selected_item.cred_pwd)
        self.controller.show_item_related_frame(self.controller.item_info_frame)
