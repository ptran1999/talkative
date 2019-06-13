from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import tkinter.font

HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 9999
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)


# Handles receiving of messages
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


# Handles sending of messages
def send(event=None):  # event is passed by binders.
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "QUIT":
        client_socket.close()
        top.quit()


# This function is to be called when the window is closed
def on_closing(event=None):
    my_msg.set("QUIT")
    send()


top = tkinter.Tk()
top.title("Talkative")

messages_frame = tkinter.Frame(top)
myFont = tkinter.font.Font(family='Helvetica', size=11)

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Enter message...")

scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, yscrollcommand=scrollbar.set, height=20, width=100)
msg_list.config(font=myFont, bg='#36393f', fg='#c8c9cb')
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=1)
msg_list.pack()
messages_frame.pack(fill=tkinter.BOTH, expand=1)

entry_field = tkinter.Entry(top, textvariable=my_msg, font=myFont,
                            insertbackground='#c8c9cb', bg='#484c52', fg='#c8c9cb')
entry_field.bind("<FocusIn>", lambda args: entry_field.delete('0', 'end'))
entry_field.bind("<Return>", send)
entry_field.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
# Enter button
send_button = tkinter.Button(top, font=myFont, text="Send", command=send, bg='#484c52', fg='#c8c9cb')
send_button.pack(ipadx=5, ipady=5, side=tkinter.LEFT, fill=tkinter.BOTH)

top.protocol("WM_DELETE_WINDOW", on_closing)


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

tkinter.mainloop()  # Starts GUI execution.