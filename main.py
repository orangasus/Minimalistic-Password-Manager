# Root of the app

from db_management import DataBaseManager
from my_tk_app import AppWindow

db_manager = DataBaseManager()
app = AppWindow(db_manager)
app.mainloop()
