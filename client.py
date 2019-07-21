from tkinter import *
from tkinter import Entry
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import font


class reg_login():
    def __init__(self, top):
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        self.HOST = '127.0.0.1'  # 'ec2-18-217-233-159.us-east-2.compute.amazonaws.com'
        self.PORT = 9999

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.client_socket.connect(self.ADDR)

        receive_thread = Thread()
        receive_thread.start()

        self.top = top
        self.Home = Frame(self.top)
        self.Login = Frame(self.top, background='#36393f')
        self.Register = Frame(self.top, background='#36393f')
        self.Chat = Frame(self.top)

        Page_list = (self.Home, self.Login, self.Register, self.Chat)

        for frame in Page_list:
            frame.grid(row=0, column=0, sticky="news")
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)

        self.top_frame(self.Home)
        self.Home_page()
        self.Login_page()
        self.Register_page()
        self.Chat_page()


    def Home_page(self):
        myFont = font.Font(family='Helvetica', size=int(x / 50))
        title = Label(self.Home, text='Talkative', font=font.Font(family='Helvetica', size=int(x / 30)), bg='#36393f', fg='#c8c9cb')
        title.pack(fill=BOTH, expand=True)
        login_button = Button(self.Home, text='Login',command=lambda:self.top_frame(self.Login), font=myFont, bg='#484c52', fg='#c8c9cb')
        login_button.pack(fill=BOTH, expand=True)
        register_button = Button(self.Home, text='Register', command=lambda: self.top_frame(self.Register), font=myFont, bg='#484c52', fg='#c8c9cb')
        register_button.pack(fill=BOTH, expand=True)

    def Login_page(self):
        for num in range(0, 5):
            self.Login.grid_rowconfigure(num, weight=1)
        for num in range(0, 2):
            self.Login.grid_columnconfigure(num, weight=1)

        myFont = font.Font(family='Helvetica', size=int(x / 50))
        Label(self.Login, text='Login', font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=0, columnspan=2)
        Label(self.Login, text="Username: ", font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=1, column=0, sticky=E)
        self.login_username_verify = StringVar()
        self.login_password_verify = StringVar()
        self.username_entry1 = Entry(self.Login, textvariable=self.login_username_verify, font=myFont, insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.username_entry1.grid(row=1, column=1, sticky=W)
        Label(self.Login, text="Password: ", font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=2, column=0, sticky=E)
        self.password_entry1 = Entry(self.Login, textvariable=self.login_password_verify, show="*", font=myFont, insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.password_entry1.grid(row=2, column=1, sticky=W)
        Button(self.Login, text='Sign in', font=myFont, bg='#484c52', fg='#c8c9cb', command=self.send_login_info).grid(row=3, columnspan=2)
        Button(self.Login, text='Cancel', font=myFont, bg='#484c52', fg='#c8c9cb', command=lambda: self.top_frame(self.Home)).grid(row=4, columnspan=2)

    def Register_page(self):
        for num in range(0, 6):
            self.Register.grid_rowconfigure(num, weight=1)
        for num in range(0, 2):
            self.Register.grid_columnconfigure(num, weight=1)

        myFont = font.Font(family='Helvetica', size=int(x / 50))
        Label(self.Register, text='Register', font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=0, columnspan=2)
        Label(self.Register, text="Username: ", font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=1, column=0, sticky=E)
        self.register_username_verify = StringVar()
        self.register_password_verify = StringVar()
        self.confirm = StringVar()
        self.username_entry2 = Entry(self.Register, textvariable=self.register_username_verify, font=myFont, insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.username_entry2.grid(row=1, column=1, sticky=W)
        Label(self.Register, text="Password: ", font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=2, column=0, sticky=E)
        self.password_entry2 = Entry(self.Register, textvariable=self.register_password_verify, show="*", font=myFont, insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.password_entry2.grid(row=2, column=1, sticky=W)
        Label(self.Register, text="Confirm Password: ", font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=3, column=0, sticky=E)
        self.confirm_pass = Entry(self.Register, textvariable=self.confirm, show="*", font=myFont, insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.confirm_pass.grid(row=3, column=1, sticky=W)
        Button(self.Register, text='Register', font=myFont, bg='#484c52', fg='#c8c9cb', command=self.send_register_info).grid(row=4, columnspan=2)
        Button(self.Register, text='Cancel', font=myFont, bg='#484c52', fg='#c8c9cb', command=lambda: self.top_frame(self.Home)).grid(row=5, columnspan=2)

    def Chat_page(self):
        self.user_frame = Frame(self.Chat)
        self.messages_frame = Frame(self.Chat)
        myFont = font.Font(family='Helvetica', size=int(x / 70))

        self.my_msg = StringVar()
        self.my_msg.set("Enter message...")

        scrollbar1 = Scrollbar(self.messages_frame)  # To navigate through past messages.

        # Following will contain the messages.
        self.msg_list = Listbox(self.messages_frame, yscrollcommand=scrollbar1.set, height=20, width=75)
        self.msg_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')
        scrollbar1.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=TOP, fill=BOTH, expand=1)
        self.messages_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        #Button(self.Chat, text='Log out', command=lambda: self.top_frame(self.Home)).pack()

        scrollbar2 = Scrollbar(self.user_frame)  # To navigate through currently connected users.
        scrollbar3 = Scrollbar(self.user_frame)

        # Connected user list
        self.tempFriend = StringVar()
        self.findUser_Entry = Entry(self.user_frame, textvariable=self.tempFriend)

        self.friend_list = Listbox(self.user_frame, yscrollcommand=scrollbar2.set, height=10, width=25)
        self.friend_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')

        self.request_list = Listbox(self.user_frame, yscrollcommand=scrollbar3.set, height=10, width=25)
        self.request_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')

        # Accept and decline button
        accept_b = Button(self.user_frame, text="Accept")
        decline_b = Button(self.user_frame, text="Decline")

        # Display data of request list
        # mycursor.execute(getFriendRequestList, self.userId)
        # temp_list = mycursor.fetchall()
        # request_tuple = ()
        #
        # for i in temp_list:
        #     request_tuple += i
        #
        # request_l = list(request_tuple)
        #
        # for i in request_l:
        #     self.request_list.insert(END, i)
        #
        # # Display data of friend list
        # mycursor.execute(getFriendList, self.userId + self.userId)
        # temp_list = mycursor.fetchall()
        # friend_tuple = ()
        #
        # for i in temp_list:
        #     friend_tuple += i
        #
        # friend_l = list(friend_tuple)
        #
        # for i in friend_l:
        #     self.friend_list.insert(END, i)
        #
        # Greetings and display user info (design later)
        Label(self.user_frame, text="Welcome, ").pack()

        # Search for other user
        Label(self.user_frame, text="Find friend: ").pack()
        self.findUser_Entry.pack()
        Button(self.user_frame, text="Search").pack()

        # Display user's friend list
        scrollbar2.pack(side=RIGHT, fill=Y)
        self.friend_list.pack(side=RIGHT, fill=BOTH, expand=1)

        # Display friend request from other users
        scrollbar3.pack(side=RIGHT, fill=Y)
        self.request_list.pack(side=RIGHT, fill=BOTH, expand=1)
        accept_b.pack(side=TOP)
        decline_b.pack(side=TOP)

        self.user_frame.pack(side=LEFT, fill=BOTH, expand=1)

        # User input field and entry button
        entry_field = Entry(self.messages_frame, textvariable=self.my_msg, font=myFont, insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        entry_field.bind("<FocusIn>", lambda args: entry_field.delete('0', 'end'))
        str_msg = self.my_msg.get()
        entry_field.bind("<Return>", self.send(str_msg))
        entry_field.pack(side=LEFT, fill=BOTH, expand=1)

        # Enter button
        send_button = Button(self.messages_frame, font=myFont, text="Send", command=self.send(str_msg), bg='#484c52', fg='#c8c9cb')
        send_button.pack(ipadx=5, ipady=5, side=RIGHT, fill=BOTH)

    def top_frame(self, frame):
        frame.tkraise()

    def send_login_info(self):
        self.send("login")

        self.login_username = self.login_username_verify.get()
        self.login_password = self.login_password_verify.get()

        self.send(self.login_username)
        self.send(self.login_password)

        result = self.client_socket.recv(self.BUFSIZ).decode()
        if result == "FAILED_LOGIN":
            self.login_fail()
        elif result == "PASS_LOGIN":
            self.login_success()
            self.top_frame(self.Chat)

    def login_fail(self):
        self.username_entry1.delete(0, END)
        self.password_entry1.delete(0, END)

        self.fail_login_screen = Toplevel(self.top)
        self.fail_login_screen.title("Talkative")
        self.fail_login_screen.geometry("300x250")
        Label(self.fail_login_screen, text="Wrong ID or password!!!", fg="red", font=("calibri", 11)).pack()
        Button(self.fail_login_screen, text="OK", command=lambda: self.delete_screen(self.fail_login_screen)).pack()

    def login_success(self):
        self.success_login_screen = Toplevel(self.top)
        self.success_login_screen.title("Talkative")
        self.success_login_screen.geometry("300x250")
        Label(self.success_login_screen, text="Successfully login!", fg="green", font=("calibri", 11)).pack()
        Button(self.success_login_screen, text="OK", command=lambda: self.delete_screen(self.success_login_screen)).pack()

    def send_register_info(self):

        self.register_username = self.register_username_verify.get()
        self.register_password = self.register_password_verify.get()
        self.register_confirm = self.confirm.get()

        if self.register_confirm == self.register_password:
            self.send("register")
            self.send(self.register_username)
            self.send(self.register_password)
            result = self.client_socket.recv(self.BUFSIZ).decode()

            if result == "FAILED_TO_REGISTER":
                self.register_fail()
            elif result == "REGISTER_SUCCESS":
                self.register_success()
                self.top_frame(self.Login)

        else:
            self.mismatch_Pass()

    def register_fail(self):
        self.username_entry2.delete(0, END)
        self.password_entry2.delete(0, END)
        self.confirm_pass.delete(0, END)

        self.fail_reg_screen = Toplevel(self.top)
        self.fail_reg_screen.title("Talkative")
        self.fail_reg_screen.geometry("300x250")
        Label(self.fail_reg_screen, text="Username already existed!!", fg="red", font=("calibri", 11)).pack()
        Button(self.fail_reg_screen, text="OK", command=lambda: self.delete_screen(self.fail_reg_screen)).pack()

    def mismatch_Pass(self):
        self.username_entry2.delete(0, END)
        self.password_entry2.delete(0, END)
        self.confirm_pass.delete(0, END)

        self.fail_reg_screen = Toplevel(self.top)
        self.fail_reg_screen.title("Talkative")
        self.fail_reg_screen.geometry("300x250")
        Label(self.fail_reg_screen, text="The passwords do not match!!", fg="red", font=("calibri", 11)).pack()
        Button(self.fail_reg_screen, text="OK", command=lambda: self.delete_screen(self.fail_reg_screen)).pack()

    def register_success(self):
        self.success_reg_screen = Toplevel(self.top)
        self.success_reg_screen.title("Talkative")
        self.success_reg_screen.geometry("300x250")
        Label(self.success_reg_screen, text="Successfully register!", fg="green", font=("calibri", 11)).pack()
        Button(self.success_reg_screen, text="OK", command=lambda: self.delete_screen(self.success_reg_screen)).pack()

    def send(self, msg, event=None):
        msg = msg.encode()
        self.client_socket.send(msg)

    def delete_screen(self, x):
        x.destroy()

if __name__ == "__main__":
    root = Tk()
    root.title("Talkative")
    x = int(root.winfo_screenwidth()/1.5)
    y = int(root.winfo_screenheight()/1.5)
    root.geometry(str(x) + 'x' + str(y))
    root.resizable(0, 0)
    reg_login(root)
    root.mainloop()
