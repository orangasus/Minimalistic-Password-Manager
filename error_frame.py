import customtkinter as ctk

import app_styling as app_style


class ErrorFrame(ctk.CTkFrame):
    def __init__(self, parent, title, msg, time_to_show):
        super().__init__(parent, fg_color=app_style.ACCENT_COLOR)

        self.title = title
        self.msg = msg
        self.time_to_show = time_to_show

        # self.title_label = ctk.CTkLabel(self, text=self.title, text_color='white',
        #                                 font=app_style.FONT_PRESET_MAIN)
        self.msg_label = ctk.CTkLabel(self, text=self.msg, text_color='white',
                                      font=app_style.FONT_PRESET_SMALL)

    def fill_frame_layout(self):
        # self.title_label.pack(padx=5, pady=5, side=ctk.LEFT)
        self.msg_label.pack(padx=5, pady=5, side=ctk.LEFT)

    def show_error_frame(self):
        self.place(anchor='ne', relx=1, rely=0, x=-10, y=10)
        self.fill_frame_layout()
        self.after(ms=self.time_to_show, func=self.hide_error_frame)

    def hide_error_frame(self):
        self.place_forget()
