from tkinter import Tk, Label, Button, Frame

class Dashboard:
    def __init__(self, master, user_info):
        self.master = master
        self.master.title("Dashboard")
        self.master.geometry("400x300")

        self.user_info = user_info

        self.create_widgets()

    def create_widgets(self):
        frame = Frame(self.master)
        frame.pack(pady=20)

        welcome_label = Label(frame, text=f"Welcome, {self.user_info['name']}!", font=("Arial", 16))
        welcome_label.pack(pady=10)

        info_label = Label(frame, text=f"Email: {self.user_info['email']}", font=("Arial", 12))
        info_label.pack(pady=5)

        exit_button = Button(frame, text="Exit", command=self.master.quit, bg="red", fg="white")
        exit_button.pack(pady=20)