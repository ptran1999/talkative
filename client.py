from tkinter import *
from tkinter import Entry
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import font
from userDB import userDB

class reg_login:

    def __init__(self):
        self.screen = Tk()
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.users = userDB()



    def main_screen(self):
        self.screen.geometry("300x250")
        self.screen.title("Talkative")
        Label(text="Talkative", bg="grey", width="300", height="2", font=("Calibri", 15)).pack()
        Label(text="").pack()
        Button(text="Login", height="2", width="30", command=self.login).pack()
        Label(text="").pack()
        Button(text="Register", height="2", width="30", command=self.register).pack()

        self.screen.protocol("WM_DELETE_WINDOW", self.on_closing)
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
        msg = self.users.username_query(temp_name[0])

        if msg:
            self.register_fail()
        else:
            self.register_success()

    def register_success(self):
        # insert temp_user to db
        self.users.user_insert(self.temp_user1[0], self.temp_user1[1])


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
        self.username_info = self.username_verify.get()
        password_info = self.password_verify.get()

        temp_user = (self.username_info, password_info)
        self.temp_username = (self.username_info,)
        self.username_entry1.delete(0, END)
        self.password_entry1.delete(0, END)

        # Query if user exist in the db
        msg = self.users.username_query(temp_user[0])


        if msg:
            self.login_success()
            self.connect()
        else:
            self.user_not_found()

    def login_success(self):
        self.screen3 = Toplevel(self.screen)
        self.screen3.title("Talkative")
        self.screen3.geometry("300x250")
        Label(self.screen3, text="Successfully login!", fg="green", font=("calibri", 11)).pack()
        Button(self.screen3, text="OK", command=self.delete0_2_3).pack()

        # TODO get userID
        self.userid = self.users.get_user_id(self.temp_username[0])
        # mycursor.execute(getUserId, self.temp_username)
        # self.userId = mycursor.fetchone()


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

    # Handles receiving of messages
    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.insert(END, msg)
            except OSError:  # Possibly client has left the chat.
                break

    # Handles sending of messages
    def send(self, event=None):  # event is passed by binders.
        msg = self.my_msg.get()
        self.my_msg.set("")  # Clears input field.
        self.client_socket.send(bytes(msg, "utf8"))
        if msg == "QUIT":
            self.client_socket.close()
            self.screen.destroy()

    # This function is to be called when the window is closed
    def on_closing(self, event=None):
        self.client_socket.close()
        self.screen.destroy()

    def connect(self):
        self.HOST = 'ec2-18-217-233-159.us-east-2.compute.amazonaws.com'
        self.PORT = 9999

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        # GUI part begin

        self.client_gui = Toplevel(self.screen)
        self.client_gui.title("Talkative")

        # Frame declarations
        self.talkative_frame = Frame(self.client_gui)
        self.user_frame = Frame(self.talkative_frame)
        self.messages_frame = Frame(self.talkative_frame)

        self.talkative_frame.pack(fill=BOTH, expand=1)
        myFont = font.Font(family='Helvetica', size=11)

        # For the messages to be sent.
        self.my_msg = StringVar()
        self.my_msg.set("Enter message...")

        scrollbar1 = Scrollbar(self.messages_frame)  # To navigate through past messages.

        # Following will contain the messages.
        self.msg_list = Listbox(self.messages_frame, yscrollcommand=scrollbar1.set, height=20, width=75)
        self.msg_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')
        scrollbar1.pack(side=RIGHT, fill=Y)
        self.msg_list.pack(side=TOP, fill=BOTH, expand=1)
        self.messages_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        # TODO reimplment all of this
        # scrollbar2 = Scrollbar(self.user_frame)  # To navigate through currently connected users.
        # scrollbar3 = Scrollbar(self.user_frame)
        #
        # # Connected user list
        # self.tempFriend = StringVar()
        # self.findUser_Entry = Entry(self.user_frame, textvariable=self.tempFriend)
        #
        # self.friend_list = Listbox(self.user_frame, yscrollcommand=scrollbar2.set, height=10, width=25)
        # self.friend_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')
        #
        # self.request_list = Listbox(self.user_frame, yscrollcommand=scrollbar3.set, height=10, width=25)
        # self.request_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')
        #
        # # Accept and decline button
        # accept_b = Button(self.user_frame, text="Accept", command=self.accept_request)
        # decline_b = Button(self.user_frame, text="Decline", command=self.decline_request)
        #
        # # Display data of request list
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
        Label(self.user_frame, text="Welcome, " + self.username_info).pack()
        #
        # # Search for other user
        # Label(self.user_frame, text="Find friend: ").pack()
        # self.findUser_Entry.pack()
        # Button(self.user_frame, text="Search", command=self.searchFriend).pack()
        #
        # # Display user's friend list
        # scrollbar2.pack(side=RIGHT, fill=Y)
        # self.friend_list.pack(side=RIGHT, fill=BOTH, expand=1)
        #
        # # Display friend request from other users
        # scrollbar3.pack(side=RIGHT, fill=Y)
        # self.request_list.pack(side=RIGHT, fill=BOTH, expand=1)
        # accept_b.pack(side=TOP)
        # decline_b.pack(side=TOP)
        #
        # self.user_frame.pack(side=LEFT, fill=BOTH, expand=1)
        #
        # User input field and entry button
        entry_field = Entry(self.messages_frame, textvariable=self.my_msg, font=myFont,
                            insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
        entry_field.bind("<FocusIn>", lambda args: entry_field.delete('0', 'end'))
        entry_field.bind("<Return>", self.send)
        entry_field.pack(side=LEFT, fill=BOTH, expand=1)

        # Enter button
        send_button = Button(self.messages_frame, font=myFont, text="Send", command=self.send, bg='#484c52',
                             fg='#c8c9cb')
        send_button.pack(ipadx=5, ipady=5, side=RIGHT, fill=BOTH)

        self.client_socket.connect(self.ADDR)

        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        self.client_gui.protocol("WM_DELETE_WINDOW", self.on_closing)

    # def searchFriend(self):
    #     # Get the input and find the user
    #     self.foundFriend = self.tempFriend.get()
    #
    #     self.findUser_Entry.delete(0, END)
    #
    #     self.temp_friend_name = (self.foundFriend,)
    #     mycursor.execute(usernameQuery, self.temp_friend_name)
    #     msg = mycursor.fetchone()
    #
    #     if msg:
    #         # Pop up if the user is found
    #         self.friendPopUp = Toplevel(self.client_gui)
    #         self.friendPopUp.geometry("200x100")
    #         Label(self.friendPopUp, text=self.foundFriend).pack()
    #         Button(self.friendPopUp, text="Add", command=self.addFriend).pack()
    #     else:
    #         # Yield error if user is not in the database
    #         self.friendPopUp = Toplevel(self.client_gui)
    #         self.friendPopUp.geometry("200x100")
    #         Label(self.friendPopUp, text="User " + self.foundFriend + " does not exist!", fg="red").pack()
    #         Button(self.friendPopUp, text="Cancel", command=self.friendPopUp.destroy).pack()
    #
    # def addFriend(self):
    #     # Get the friend id and check if already add
    #     mycursor.execute(getUserId, self.temp_friend_name)
    #     friendId = mycursor.fetchone()
    #
    #     exist_rela = self.userId + friendId + self.userId + friendId
    #     request = self.userId + friendId + (0,)
    #
    #     mycursor.execute(relationshipQuery, exist_rela)
    #     msg = mycursor.fetchall()
    #
    #     if msg:
    #         # Error if already add this person
    #         Label(self.friendPopUp, text="Already add " + self.foundFriend + " !!!", fg="red").pack()
    #         Button(self.friendPopUp, text="OK", command=self.friendPopUp.destroy).pack()
    #     else:
    #         if friendId != self.userId:
    #             mycursor.execute(addFriend, request)
    #             db.commit()
    #             Label(self.friendPopUp, text="Successfully add friend!", fg="green").pack()
    #             Button(self.friendPopUp, text="OK", command=self.friendPopUp.destroy).pack()
    #         else:
    #             # Error trying to add oneself
    #             Label(self.friendPopUp, text="Cannot add yourself!", fg="red").pack()
    #             Button(self.friendPopUp, text="OK", command=self.friendPopUp.destroy).pack()
    #
    # def accept_request(self):
    #     # Switch status in relationship database from 0 to 1
    #     select = self.request_list.curselection()
    #     for i in select:
    #         temp = (self.request_list.get(i),)
    #         mycursor.execute(getUserId, temp)
    #         tempId = mycursor.fetchone()
    #         mycursor.execute(acceptRequest, tempId + self.userId)
    #         db.commit()
    #         self.request_list.delete(i)
    #     self.friend_list.insert(END, temp)
    #
    # def decline_request(self):
    #     # Delete the relationship row if the request is decline
    #     select = self.request_list.curselection()
    #     for i in select:
    #         temp = (self.request_list.get(i),)
    #         mycursor.execute(getUserId, temp)
    #         tempId = mycursor.fetchone()
    #         mycursor.execute(declineRequest, tempId + self.userId)
    #         db.commit()
    #         self.request_list.delete(i)


if __name__ == "__main__":
    obj = reg_login()
    obj.main_screen()