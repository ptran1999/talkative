from tkinter import *
from tkinter import Entry
from mydatabase import *


class reg_log:

    def __init__(self):
        self.flag = False

    def main_screen(self):
        self.screen = Tk()
        self.screen.geometry("300x250")
        self.screen.title("Talkative")
        Label(text="Talkative", bg="grey", width="300", height="2", font=("Calibri", 15)).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30", command=self.login).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="30", command=self.register).pack()

        self.screen.mainloop()

    # Register part
    def register(self):
        self.screen1 = Toplevel(self.screen)
        self.screen1.title("Talkative")
        self.screen1.geometry("300x250")

        self.username = StringVar()
        self.password = StringVar()

        Label(self.screen1, text="Register").pack()
        Label(self.screen1, text="").pack()

        # Send info to <***>_entry variables for later use
        Label(self.screen1, text="Username * ").pack()
        self.username_entry = Entry(self.screen1, textvariable=self.username)
        self.username_entry.pack()
        Label(self.screen1, text="Password * ").pack()
        self.password_entry = Entry(self.screen1, textvariable=self.password)
        self.password_entry.pack()
        Label(self.screen1, text="").pack()

        # Go to register_user when done
        Button(self.screen1, text="Register", width=10, height=1, command=self.register_user).pack()

    def register_user(self):
        # get the info from register and put it to a temp_user
        username_info = self.username.get()
        password_info = self.password.get()

        self.temp_user1 = (username_info, password_info)
        temp_name = (username_info,)

        # Query if username already exist in the db
        mycursor.execute(usernameQuery, temp_name)
        msg = mycursor.fetchone()

        if msg:
            self.register_fail()
        else:
            self.register_success()

    def register_success(self):
        # insert temp_user to db
        mycursor.execute(userInsert, self.temp_user1)
        db.commit()

        self.screen5 = Toplevel(self.screen)
        self.screen5.title("Talkative")
        self.screen5.geometry("300x250")
        Label(self.screen5, text="Successfully register!", fg="green", font=("calibri", 11)).pack()
        Button(self.screen5, text="OK", command=self.delete1_5).pack()

    def register_fail(self):
        # refresh the input for next incoming info
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)

        self.screen6 = Toplevel(self.screen)
        self.screen6.title("Talkative")
        self.screen6.geometry("300x250")
        Label(self.screen6, text="Username already existed!!", fg="red", font=("calibri", 11)).pack()
        Button(self.screen6, text="OK", command=self.delete6).pack()

    # Login part
    # Everything is the same concept with register
    def login(self):
        self.screen2 = Toplevel(self.screen)
        self.screen2.title("Talkative")
        self.screen2.geometry("300x250")
        Label(self.screen2, text="Login").pack()
        Label(self.screen2, text="").pack()

        # use different variables to avoid confusion

        self.username_verify = StringVar()
        self.password_verify = StringVar()

        Label(self.screen2, text="Username * ").pack()
        self.username_entry1 = Entry(self.screen2, textvariable=self.username_verify)
        self.username_entry1.pack()
        Label(self.screen2, text="").pack()
        Label(self.screen2, text="Password * ").pack()
        self.password_entry1 = Entry(self.screen2, textvariable=self.password_verify)
        self.password_entry1.pack()
        Label(self.screen2, text="").pack()

        # Go to login_verify when done
        Button(self.screen2, text="Login", width=10, height=1, command=self.login_verify).pack()

    def login_verify(self):
        username_info = self.username_verify.get()
        password_info = self.password_verify.get()

        temp_user = (username_info, password_info)

        self.username_entry1.delete(0, END)
        self.password_entry1.delete(0, END)

        # Query if user exist in the db
        mycursor.execute(userQuery, temp_user)
        msg = mycursor.fetchone()

        if msg:
            self.login_success()
            self.flag = True
        else:
            self.user_not_found()

    def login_success(self):
        self.screen3 = Toplevel(self.screen)
        self.screen3.title("Talkative")
        self.screen3.geometry("300x250")
        Label(self.screen3, text="Successfully login!", fg="green", font=("calibri", 11)).pack()
        Button(self.screen3, text="OK", command=self.delete0_2_3).pack()
        self.screen.destroy()

    def user_not_found(self):
        self.screen4 = Toplevel(self.screen)
        self.screen4.title("Talkative")
        self.screen4.geometry("300x250")
        Label(self.screen4, text="User Not Found", fg="red", font=("calibri", 11)).pack()
        Button(self.screen4, text="OK", command=self.delete4).pack()

    def delete1_5(self):
        self.screen1.destroy()
        self.screen5.destroy()

    def delete0_2_3(self):
        self.screen2.destroy()
        self.screen3.destroy()

    def delete3(self):
        self.screen3.destroy()

    def delete4(self):
        self.screen4.destroy()

    def delete6(self):
        self.screen6.destroy()

