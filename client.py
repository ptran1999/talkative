from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter import font, Tk, Listbox


# Handles receiving of messages
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(END, msg)
        except OSError:  # Possibly client has left the chat.
            break


# Handles sending of messages
def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "QUIT":
        client_socket.close()
        client_gui.quit()


# This function is to be called when the window is closed
def on_closing(event=None):
    my_msg.set("QUIT")
    send()


def main_GUI():
    # Input Host and Port
    global HOST
    global PORT
    HOST = '127.0.0.1'
    PORT = 9999

    global BUFSIZ
    BUFSIZ = 1024
    global ADDR
    ADDR = (HOST, PORT)

    # GUI part begin
    global client_gui
    client_gui = Tk()
    client_gui.title("Talkative")
    # Frame declarations
    talkative_frame = Frame(client_gui)
    user_frame = Frame(talkative_frame)
    messages_frame = Frame(talkative_frame)

    talkative_frame.pack(fill=BOTH, expand=1)
    myFont = font.Font(family='Helvetica', size=11)

    global my_msg  # For the messages to be sent.
    my_msg = StringVar()
    my_msg.set("Enter message...")

    scrollbar1 = Scrollbar(messages_frame)  # To navigate through past messages.

    # Following will contain the messages.
    global msg_list
    msg_list = Listbox(messages_frame, yscrollcommand=scrollbar1.set, height=20, width=75)
    msg_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')
    scrollbar1.pack(side=RIGHT, fill=Y)
    msg_list.pack(side=TOP, fill=BOTH, expand=1)
    messages_frame.pack(side=RIGHT, fill=BOTH, expand=1)

    scrollbar2 = Scrollbar(user_frame)  # To navigate through currently connected users.

    # Connected user list
    user_list = Listbox(user_frame, yscrollcommand=scrollbar2.set, height=20, width=25)
    user_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')
    scrollbar2.pack(side=RIGHT, fill=Y)
    user_list.pack(side=RIGHT, fill=BOTH, expand=1)
    user_frame.pack(side=LEFT, fill=BOTH, expand=1)

    # User input field and entry button
    entry_field = Entry(messages_frame, textvariable=my_msg, font=myFont,
                        insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
    entry_field.bind("<FocusIn>", lambda args: entry_field.delete('0', 'end'))
    entry_field.bind("<Return>", send)
    entry_field.pack(side=LEFT, fill=BOTH, expand=1)

    # Enter button
    send_button = Button(messages_frame, font=myFont, text="Send", command=send, bg='#484c52', fg='#c8c9cb')
    send_button.pack(ipadx=5, ipady=5, side=RIGHT, fill=BOTH)

    client_gui.protocol("WM_DELETE_WINDOW", on_closing)

    global client_socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()

    mainloop()
main_GUI()