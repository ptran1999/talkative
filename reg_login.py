from tkinter import *
from tkinter import Entry
from mydatabase import *


# Register part
def register():
    global screen1
    screen1 = Toplevel(screen)
    screen1.title("Talkative")
    screen1.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(screen1, text="Register").pack()
    Label(screen1, text="").pack()

    # Send info to <***>_entry variables for later use
    Label(screen1, text="Username * ").pack()
    username_entry = Entry(screen1, textvariable=username)
    username_entry.pack()
    Label(screen1, text="Password * ").pack()
    password_entry = Entry(screen1, textvariable=password)
    password_entry.pack()
    Label(screen1, text="").pack()

    # Go to register_user when done
    Button(screen1, text="Register", width=10, height=1, command=register_user).pack()


def register_user():
    print("working")

    # get the info from register and put it to a temp_user
    username_info = username.get()
    password_info = password.get()

    global temp_user1
    temp_user1 = (username_info, password_info)
    temp_name = (username_info,)

    # Query if username already exist in the db
    mycursor.execute(usernameQuery, temp_name)
    msg = mycursor.fetchone()

    if msg:
        register_fail()
    else:
        register_success()


def register_success():
    # insert temp_user to db
    mycursor.execute(userInsert, temp_user1)
    db.commit()

    global screen5
    screen5 = Toplevel(screen)
    screen5.title("Talkative")
    screen5.geometry("300x250")
    Label(screen5, text="Successfully register!", fg="green", font=("calibri", 11)).pack()
    Button(screen5, text="OK", command=delete1_5).pack()


def register_fail():
    # refresh the input for next incoming info
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    global screen6
    screen6 = Toplevel(screen)
    screen6.title("Talkative")
    screen6.geometry("300x250")
    Label(screen6, text="Username already existed!!", fg="red", font=("calibri", 11)).pack()
    Button(screen6, text="OK", command=delete6).pack()


# Login part
# Everything is the same concept with register
def login():
    global screen2
    screen2 = Toplevel(screen)
    screen2.title("Talkative")
    screen2.geometry("300x250")
    Label(screen2, text="Login").pack()
    Label(screen2, text="").pack()

    # use different variables to avoid confusion
    global username_verify
    global password_verify
    global username_entry1
    global password_entry1

    username_verify = StringVar()
    password_verify = StringVar()

    Label(screen2, text="Username * ").pack()
    username_entry1 = Entry(screen2, textvariable=username_verify)
    username_entry1.pack()
    Label(screen2, text="").pack()
    Label(screen2, text="Password * ").pack()
    password_entry1 = Entry(screen2, textvariable=password_verify)
    password_entry1.pack()
    Label(screen2, text="").pack()

    # Go to login_verify when done
    Button(screen2, text="Login", width=10, height=1, command=login_verify).pack()


def login_verify():
    username_info = username_verify.get()
    password_info = password_verify.get()

    temp_user = (username_info, password_info)

    username_entry1.delete(0, END)
    password_entry1.delete(0, END)

    # Query if user exist in the db
    mycursor.execute(userQuery, temp_user)
    msg = mycursor.fetchone()

    if msg:
        login_success()
    else:
        user_not_found()


def login_success():
    global screen3
    screen3 = Toplevel(screen)
    screen3.title("Talkative")
    screen3.geometry("300x250")
    Label(screen3, text="Successfully login!", fg="green", font=("calibri", 11)).pack()
    Button(screen3, text="OK", command=delete0_2_3).pack()


def user_not_found():
    global screen4
    screen4 = Toplevel(screen)
    screen4.title("Talkative")
    screen4.geometry("300x250")
    Label(screen4, text="User Not Found", fg="red", font=("calibri", 11)).pack()
    Button(screen4, text="OK", command=delete4).pack()


def delete1_5():
    screen1.destroy()
    screen5.destroy()


def delete0_2_3():
    screen2.destroy()
    screen3.destroy()


def delete3():
    screen3.destroy()


def delete4():
    screen4.destroy()


def delete6():
    screen6.destroy()


def main_screen():
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title("Talkative")
    Label(text="Talkative", bg="grey", width="300", height="2", font=("Calibri", 15)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    screen.mainloop()
