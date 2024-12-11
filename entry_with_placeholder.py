import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, parent, entry_str_var, pl_text):
        super().__init__(parent)

        self.touched = False

        self.pl_text = pl_text
        self.text_color = 'black'
        self.pl_color = 'grey'
        self.configure(textvariable=entry_str_var, fg=self.pl_color)

        self.bind('<FocusIn>', self.on_entry_focus_in)
        self.bind('<FocusOut>', self.on_entry_focus_out)

        self.show_placeholder()

    def on_entry_focus_in(self, event):
        if not self.touched:
            self.delete(0, 'end')
            self.configure(fg=self.text_color)

    def on_entry_focus_out(self, event):
        if self.get() == '':
            self.touched = False
            self.configure(fg=self.pl_color)
            self.show_placeholder()
        else:
            self.touched = True

    def show_placeholder(self):
        self.delete(0, 'end')
        self.insert('end', self.pl_text)
