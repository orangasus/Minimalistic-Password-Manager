import customtkinter as ctk

import app_styling


class CtkListView(ctk.CTkScrollableFrame):
    def __init__(self, parent, list_of_widget_items):
        super().__init__(parent, fg_color='white', scrollbar_button_color=app_styling.BACKGROUND_GREY_COLOR)
        self.content_list = list_of_widget_items
        self.cur_selected_item_frame = None

        self.grid_columnconfigure(0, weight=1)

    def upload_all_items_to_list_view(self):
        for i, el in enumerate(self.content_list):
            self.grid_rowconfigure(i, weight=0)
            el.grid(row=i, column=0, pady=0, sticky='we')

    def delete_all_items_from_list_view(self):
        for el in self.content_list:
            el.grid_forget()

    def refresh_list_view(self):
        self.delete_all_items_from_list_view()
        self.upload_all_items_to_list_view()