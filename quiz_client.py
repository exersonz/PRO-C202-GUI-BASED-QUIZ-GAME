import socket
from threading import Thread
from tkinter import *

# asking user to choose a nickname
# nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# defining ip address and port number on which the server will run
ip_address = '127.0.0.1'
port = 8000

# connect client to server
client.connect((ip_address, port))

'''
def receive():
    while True:
        try:
            message = client.recv(2048).decode('utf-8') # decoding the encrypted message
            
            # checking if the received message is NICKNAME
            if message == 'NICKNAME':
                # sending server the user's nickname
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error occured")
            client.close() # closing client socket
            break

# function to receive message from user that needs to be sent to server
def write():
    while True:
        message = '{}:{}'.format(nickname, input(''))
        client.send(message.encode('utf-8'))

receive_thread = Thread(target=receive)
receive_thread.start()

write_thread = Thread(target=write)
write_thread.start()
'''

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw() # withdrawing the quiz screen initially

        self.login = Toplevel() # making the login screen come ON TOP quiz screen
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300, bg="#d8e2eb")

        self.loginTitle = Label(self.login, text="Please login to continue", justify=CENTER, font="Courier 14 bold", bg="#d8e2eb")
        self.loginTitle.place(relheight=0.15, relx=0.15, rely=0.07)
        
        self.label = Label(self.login, text="Enter your name: ", font="Courier 12", bg="#d8e2eb")
        self.label.place(relheight=0.2, relx=0.08, rely=0.2)

        self.entryName = Entry(self.login, font="Courier 12")
        self.entryName.place(relwidth=0.4, relheight=0.1, relx=0.5, rely=0.25)
        self.entryName.focus()

        self.button = Button(self.login, text="CONTINUE", font="Courier 14", bg="#8897aa", command= lambda: self.goAhead(self.entryName.get()))
        self.button.place(relx=0.3, rely=0.5)

        self.Window.mainloop()
    
    def goAhead(self, name):
        self.login.destroy()
        self.name = name # saving user name

        # starting thread and calling receive function
        rcv = Thread(target=self.receive)
        rcv.start()

    # function to receive the messages sent from server
    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8') # decoding the encrypted message
                
                # checking if the received message is NICKNAME
                if message == 'NICKNAME':
                    # sending server the user's nickname
                    client.send(self.name.encode('utf-8'))
                else:
                    pass # adding this since we don't want to print in the terminal
            except:
                print("Error occured")
                client.close() # closing client socket
                break
    
g = GUI() # creating a object for GUI class
# init function will be called as soon as we are creating the object