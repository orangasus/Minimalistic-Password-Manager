# Abstract class used as a parent
# most frames in the program


import customtkinter as ctk


class StandardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color='white')
        self.controller = controller
        self.db_manager = self.controller.db_manager
