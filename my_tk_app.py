# Class implementing app's main window
# and general logic

from content_related_frames import *
from cred_item import CredItem
from user_related_frames import *


class AppWindow(ctk.CTk):
    def __init__(self, db_manager):
        super().__init__()
        self.geometry(app_style.APP_GEOMETRY)
        self.title(app_style.APP_TITLE)
        self.db_manager = db_manager
        self.app_state = {'cur_user': None}
        self.resizable(False, False)

        self.frame_container = ctk.CTkFrame(self)

        self.frame_container.pack(expand=True, fill='both')

        self.frames_list = []

        self.user_items_list = []

        self.add_list_item_frame = None
        self.login_form_frame = None
        self.create_user_frame = None
        self.user_content_frame = None

        self.initialize_all_frames()
        self.add_all_frames_to_grid()

        self.show_frame(self.login_form_frame)

    def initialize_all_frames(self):
        self.add_list_item_frame = AddListItemFrame(self.frame_container, self)
        self.login_form_frame = LoginIntoAppFrame(self.frame_container, self)
        self.create_user_frame = CreateUserFrame(self.frame_container, self)
        self.user_content_frame = UserContentFrame(self.frame_container, self)

        self.frames_list.extend([self.add_list_item_frame, self.login_form_frame,
                                 self.create_user_frame, self.user_content_frame])

    def add_all_frames_to_grid(self):
        self.frame_container.grid_rowconfigure(0, weight=1)
        self.frame_container.grid_columnconfigure(0, weight=1)
        for frame in self.frames_list:
            frame.grid(row=0, column=0, sticky='news')

    def show_frame(self, frame):
        frame.tkraise()

    def fill_user_items_list(self):
        self.user_items_list = []
        db_items = self.db_manager.cred_table_manager.get_all_creds_items_by_user(self.app_state['cur_user'])
        if db_items is not None:
            for item in db_items:
                self.user_items_list.append(CredItem(item))
