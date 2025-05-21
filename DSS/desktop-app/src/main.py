from tkinter import Tk
from registration import Registration

def main():
    root = Tk()
    root.title("Desktop Application")
    root.geometry("400x300")

    # Start the registration process
    registration = Registration(root)
    registration.start_registration()

    root.mainloop()

if __name__ == "__main__":
    main()