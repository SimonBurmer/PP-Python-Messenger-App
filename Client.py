from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import sys


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            message = client_socket.recv(BUFSIZ).decode("utf8") # recv message from server
            messages_list.insert(tkinter.END, message) # add message to the end of the messages list
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by tk binders.
    """Handles sending of messages."""
    msg = my_message.get() # Gets message from input field.
    my_message.set("")  # Sets input field to "".
    client_socket.send(bytes(msg, "utf8")) # Sends message to server.
    if msg == "{quit}":
        client_socket.close()
        client_GUI.destroy()

def on_closing(event=None):
    """This function is to be called when the window is closed."""
    if connected:
        my_message.set("{quit}")
        send()
    else:
        client_GUI.destroy()
        sys.exit()


#----------GUI---------
client_GUI = tkinter.Tk()
client_GUI.title("Simons Messenger")
messages_frame = tkinter.Frame(client_GUI)
my_message = tkinter.StringVar()  # For the messages to be sent.
my_message.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame) # To navigate through past messages.

messages_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
messages_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
messages_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(client_GUI, textvariable=my_message)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(client_GUI, text="Send", command=send)
send_button.pack()

client_GUI.protocol("WM_DELETE_WINDOW", on_closing)


#----Now comes the sockets part----
connected = False
HOST = input('Enter host: ')
PORT = input('Enter port: ')
BUFSIZ = 1024

if not HOST:
    HOST = "127.0.0.1"
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
connected = True

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
