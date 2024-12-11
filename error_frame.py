import tkinter as tk


class ErrorFrame(tk.Frame):
    def __init__(self, parent, controller, title, msg, time_to_show):
        super().__init__(parent)

        self.controller = controller

        self.configure(width='50px', height='20px', bg='red')

        self.title = title
        self.msg = msg
        self.time_to_show = time_to_show

        self.title_label = tk.Label(self, text = self.title,bg='red', fg='white')
        self.msg_label = tk.Label(self, text=self.msg, bg='red', fg='white')

        self.fill_frame_layout()

    def fill_frame_layout(self):
        self.title_label.pack()
        self.msg_label.pack()

    def show_error_frame(self):
        self.grid(row=0, column=3, sticky='ne')
        self.tkraise()
        self.after(self.time_to_show, self.hide_error_frame)

    def hide_error_frame(self):
        self.grid_forget()
