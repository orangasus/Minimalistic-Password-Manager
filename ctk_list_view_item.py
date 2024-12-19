# Class that represents list of
# saved credentials items in UI

import customtkinter as ctk

import app_styling as app_style


class CtkListViewItem(ctk.CTkFrame):
    hover_color = app_style.HOVER_HIGHLIGHT_COLOR
    stand_color = 'transparent'
    indicator_color = app_style.ACCENT_COLOR

    def __init__(self, parent, controller, cred_item_obj, item_ind):
        super().__init__(parent, fg_color='white')
        self.parent = parent
        self.cred_item_obj = cred_item_obj
        self.controller = controller
        self.item_ind = item_ind

        self.cred_name_label = ctk.CTkLabel(self, text=cred_item_obj.cred_name, font=app_style.FONT_PRESET_MAIN)
        self.cred_login_label = ctk.CTkLabel(self, text=cred_item_obj.cred_login, font=app_style.FONT_PRESET_SMALL)
        self.select_indicator_frame = ctk.CTkFrame(self, fg_color=self.stand_color, width=5, height=0)

        self.bind('<Button-1>', self.on_click)
        self.cred_name_label.bind('<Button-1>', self.on_click)
        self.cred_login_label.bind('<Button-1>', self.on_click)

        self.bind('<Enter>', self.on_hover_enter)
        self.bind('<Leave>', self.on_hover_leave)

        self.cred_login_label.bind('<Enter>', self.on_hover_enter)
        self.cred_login_label.bind('<Leave>', self.on_hover_leave)
        self.cred_name_label.bind('<Enter>', self.on_hover_enter)
        self.cred_name_label.bind('<Leave>', self.on_hover_leave)

        self.fill_grid_layout()

    def fill_grid_layout(self):
        self.cred_name_label.grid(row=0, column=1, padx=5, pady=1, sticky='ws')
        self.cred_login_label.grid(row=1, column=1, padx=5, pady=1, sticky='wn')
        self.select_indicator_frame.grid(row=0, rowspan=2, column=0, padx=0, pady=1, sticky='ns')

    def on_click(self, event):
        self.controller.user_content_state['cur_item_ind'] = self.item_ind
        selected_item = self.cred_item_obj
        if self.parent.cur_selected_item_frame is not None:
            self.parent.cur_selected_item_frame.change_select_indicator_color_to_stand()

        self.parent.cur_selected_item_frame = self
        self.select_indicator_frame.configure(fg_color=self.indicator_color)

        self.controller.item_info_frame.update_labels_info(selected_item.cred_name,
                                                           selected_item.cred_login,
                                                           selected_item.cred_pwd)
        self.controller.show_item_related_frame(self.controller.item_info_frame)

    def change_select_indicator_color_to_stand(self):
        self.select_indicator_frame.configure(fg_color=self.stand_color)

    def on_hover_enter(self, event):
        self.configure(fg_color=self.hover_color)

    def on_hover_leave(self, event):
        self.configure(fg_color=self.stand_color)
