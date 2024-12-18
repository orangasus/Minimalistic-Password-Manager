import tkinter as tk
import customtkinter as ctk
import app_styling as app_style


class StandardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color='white')
        self.controller = controller
        self.db_manager = self.controller.db_manager
