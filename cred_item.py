class CredItem:
    def __init__(self, db_entry):
        self.db_id = db_entry[0]
        self.user = db_entry[1]
        self.cred_name = db_entry[2]
        self.cred_login = db_entry[3]
        self.cred_pwd = db_entry[4]

    def __str__(self):
        return f"""
        ID: {self.db_id}
        USER: {self.user}
        NAME: {self.cred_name}
        LOGIN: {self.cred_login}
        PASSWORD: {self.cred_pwd}
        """