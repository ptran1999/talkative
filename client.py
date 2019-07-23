from tkinter import *
from tkinter import Entry
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import font
from time import sleep
import os

class reg_login():
    def __init__(self, top):
        self.client_socket = socket(AF_INET, SOCK_STREAM)

        self.HOST = 'ec2-3-14-66-181.us-east-2.compute.amazonaws.com'
        # self.HOST = '127.0.0.1'  # 'ec2-18-217-233-159.us-east-2.compute.amazonaws.com'
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
        title = Label(self.Home, text='Talkative', font=font.Font(family='Helvetica', size=int(x / 30)), bg='#36393f',
                      fg='#c8c9cb')
        title.pack(fill=BOTH, expand=True)
        login_button = Button(self.Home, text='Login', command=lambda: self.top_frame(self.Login), font=myFont,
                              bg='#484c52', fg='#c8c9cb')
        login_button.pack(fill=BOTH, expand=True)
        register_button = Button(self.Home, text='Register', command=lambda: self.top_frame(self.Register), font=myFont,
                                 bg='#484c52', fg='#c8c9cb')
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
        self.username_entry1 = Entry(self.Login, textvariable=self.login_username_verify, font=myFont,
                                     insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.username_entry1.grid(row=1, column=1, sticky=W)
        Label(self.Login, text="Password: ", font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=2, column=0, sticky=E)
        self.password_entry1 = Entry(self.Login, textvariable=self.login_password_verify, show="*", font=myFont,
                                     insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.password_entry1.grid(row=2, column=1, sticky=W)
        Button(self.Login, text='Sign in', font=myFont, bg='#484c52', fg='#c8c9cb', command=self.send_login_info).grid(
            row=3, columnspan=2)
        Button(self.Login, text='Cancel', font=myFont, bg='#484c52', fg='#c8c9cb',
               command=lambda: self.top_frame(self.Home)).grid(row=4, columnspan=2)

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
        self.username_entry2 = Entry(self.Register, textvariable=self.register_username_verify, font=myFont,
                                     insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.username_entry2.grid(row=1, column=1, sticky=W)
        Label(self.Register, text="Password: ", font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=2, column=0, sticky=E)
        self.password_entry2 = Entry(self.Register, textvariable=self.register_password_verify, show="*", font=myFont,
                                     insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.password_entry2.grid(row=2, column=1, sticky=W)
        Label(self.Register, text="Confirm Password: ", font=myFont, bg='#36393f', fg='#c8c9cb').grid(row=3, column=0,
                                                                                                      sticky=E)
        self.confirm_pass = Entry(self.Register, textvariable=self.confirm, show="*", font=myFont,
                                  insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        self.confirm_pass.grid(row=3, column=1, sticky=W)
        Button(self.Register, text='Register', font=myFont, bg='#484c52', fg='#c8c9cb',
               command=self.send_register_info).grid(row=4, columnspan=2)
        Button(self.Register, text='Cancel', font=myFont, bg='#484c52', fg='#c8c9cb',
               command=lambda: self.top_frame(self.Home)).grid(row=5, columnspan=2)

    def Chat_page(self):
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

        # User input field and entry button
        entry_field = Entry(self.messages_frame, textvariable=self.my_msg, font=myFont, insertbackground='#c8c9cb',
                            bg='#484c52', fg='#c8c9cb')
        entry_field.bind("<FocusIn>", lambda args: entry_field.delete('0', 'end'))
        if self.my_msg.get() != "Enter message...":
            str_msg = self.my_msg.get()
        else:
            str_msg = ""
        entry_field.bind("<Return>", lambda send: (self.send(str_msg), sleep(.1), entry_field.delete('0', 'end')))
        entry_field.pack(side=LEFT, fill=BOTH, expand=1)
        # Enter button
        send_button = Button(self.messages_frame, font=myFont, text="Send", command=lambda: self.send(str_msg),
                             bg='#484c52', fg='#c8c9cb')
        send_button.pack(ipadx=5, ipady=5, side=RIGHT, fill=BOTH)

    def top_frame(self, frame):
        frame.tkraise()

    def send_login_info(self):
        self.send("LOGIN")

        self.login_username = self.login_username_verify.get()
        self.login_password = self.login_password_verify.get()

        if self.login_username != "" and self.login_password != "":
            self.send(self.login_username)
            self.send(self.login_password)

            result = self.client_socket.recv(self.BUFSIZ).decode('utf8')
            if result == "FAILED_LOGIN":
                self.login_fail()
            elif result == "PASS_LOGIN":
                self.login_success()
                self.top_frame(self.Chat)
        else:
            self.blank_entry()

    def blank_entry(self):
        myFont = font.Font(family='Helvetica', size=int(x / 50))
        self.username_entry1.delete(0, END)
        self.password_entry1.delete(0, END)

        self.fail_login_screen = Toplevel(self.top)
        self.fail_login_screen.title("Talkative")
        self.fail_login_screen.geometry(str(int(x / 2)) + 'x' + str(int(y / 2)))
        self.fail_login_screen.config(background='#36393f')
        Label(self.fail_login_screen, text="There was at least one empty line.", bg='#36393f', fg="red",
              font=myFont).pack(expand=True)
        Button(self.fail_login_screen, text="OK", font=myFont, bg='#484c52', fg='#c8c9cb',
               command=lambda: self.delete_screen(self.fail_login_screen)).pack(expand=True)

    def login_fail(self):
        myFont = font.Font(family='Helvetica', size=int(x / 50))
        self.username_entry1.delete(0, END)
        self.password_entry1.delete(0, END)

        self.fail_login_screen = Toplevel(self.top)
        self.fail_login_screen.title("Talkative")
        self.fail_login_screen.geometry(str(int(x/2)) + 'x' + str(int(y/2)))
        self.fail_login_screen.config(background='#36393f')
        Label(self.fail_login_screen, text="Incorrect Username/Password.", bg='#36393f', fg="red",
              font=myFont).pack(expand=True)
        Button(self.fail_login_screen, text="OK", font=myFont, bg='#484c52', fg='#c8c9cb',
               command=lambda: self.delete_screen(self.fail_login_screen)).pack(expand=True)

    def login_success(self):
        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def send_register_info(self):

        self.register_username = self.register_username_verify.get()
        self.register_password = self.register_password_verify.get()
        self.register_confirm = self.confirm.get()

        if self.register_username != "" and self.register_password != "" and self.register_confirm != "":

            if self.register_confirm == self.register_password:
                self.send("REGISTER")

                # self.client_socket.send(bytes(self.register_username, 'utf8'))
                # self.client_socket.send(bytes(self.register_password, 'utf8'))
                self.send(self.register_username)
                self.send(self.register_password)
                result = self.client_socket.recv(self.BUFSIZ).decode('utf')

                if result == "FAILED_TO_REGISTER":
                    self.register_fail()
                elif result == "REGISTER_SUCCESS":
                    self.register_success()
                    self.top_frame(self.Login)

            else:
                self.mismatch_Pass()
        else:
            self.blank_entry()

    def register_fail(self):
        self.username_entry2.delete(0, END)
        self.password_entry2.delete(0, END)
        self.confirm_pass.delete(0, END)
        myFont = font.Font(family='Helvetica', size=int(x / 50))

        self.fail_reg_screen = Toplevel(self.top)
        self.fail_reg_screen.title("Talkative")
        self.fail_reg_screen.geometry(str(int(x / 2)) + 'x' + str(int(y / 2)))
        self.fail_reg_screen.config(background='#36393f')
        Label(self.fail_reg_screen, text="That username already exists.\n Try again.", bg='#36393f', fg="red",
              font=myFont).pack(expand=True)
        Button(self.fail_reg_screen, text="OK", font=myFont, bg='#484c52', fg='#c8c9cb',
               command=lambda: self.delete_screen(self.fail_reg_screen)).pack(expand=True)

    def mismatch_Pass(self):
        self.username_entry2.delete(0, END)
        self.password_entry2.delete(0, END)
        self.confirm_pass.delete(0, END)
        myFont = font.Font(family='Helvetica', size=int(x / 50))

        self.fail_reg_screen = Toplevel(self.top)
        self.fail_reg_screen.title("Talkative")
        self.fail_reg_screen.geometry(str(int(x / 2)) + 'x' + str(int(y / 2)))
        self.fail_reg_screen.config(background='#36393f')
        Label(self.fail_reg_screen, text="Passwords do not match.", bg='#36393f', fg="red",
              font=myFont).pack(expand=True)
        Button(self.fail_reg_screen, text="OK", font=myFont, bg='#484c52', fg='#c8c9cb',
               command=lambda: self.delete_screen(self.fail_reg_screen)).pack(expand=True)

    def register_success(self):
        myFont = font.Font(family='Helvetica', size=int(x / 50))
        self.success_reg_screen = Toplevel(self.top)
        self.success_reg_screen.title("Talkative")
        self.success_reg_screen.geometry(str(int(x / 2)) + 'x' + str(int(y / 2)))
        self.success_reg_screen.config(background='#36393f')
        Label(self.success_reg_screen, text="Successfully registered.", bg='#36393f', fg="green",
              font=myFont).pack(expand=True)
        Button(self.success_reg_screen, text="OK", font=myFont, bg='#484c52', fg='#c8c9cb',
               command=lambda: self.delete_screen(self.success_reg_screen)).pack(expand=True)

    def send(self, msg, event=None):
        check_msg = self.my_msg.get()
        if check_msg != "Enter message...":
            msg = check_msg
            print(msg)
        sleep(.5)
        self.client_socket.send(bytes(msg, 'utf8'))
        if msg == "QUIT":
            os._exit(0)

    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode('utf8')
                self.msg_list.insert(END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    def delete_screen(self, x):
        x.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Talkative")
    x = int(root.winfo_screenwidth()/1.5)
    y = int(root.winfo_screenwidth()/2.67)
    root.geometry(str(x) + 'x' + str(y))
    # root.resizable(0, 0)
    reg_login(root)
    root.mainloop()
