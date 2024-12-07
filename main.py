from my_tk_app import AppWindow
from db_management import DataBaseManager

db_manager = DataBaseManager()
app = AppWindow(db_manager)
app.mainloop()