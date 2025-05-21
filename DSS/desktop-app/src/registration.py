class Registration:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def validate_input(self, username, password):
        if not username or not password:
            return False, "Username and password cannot be empty."
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        return True, ""

    def save_user(self, username, password):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.db_connection.commit()
            return True, "Registration successful."
        except Exception as e:
            return False, str(e)
        finally:
            cursor.close()

    def register_user(self, username, password):
        is_valid, message = self.validate_input(username, password)
        if not is_valid:
            return False, message
        
        return self.save_user(username, password)