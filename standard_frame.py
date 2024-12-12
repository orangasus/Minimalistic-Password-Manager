import tkinter as tk
import customtkinter as ctk


class StandardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db_manager = self.controller.db_manager
