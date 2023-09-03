import socket
from threading import Thread
import random

# creating a server with AF_INET and SOCK_STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# defining ip address & port num on which server will run on
ip_address = '127.0.0.1'
port = 8000

# binding server to ip address & port
server.bind((ip_address, port))

# making the server listen to incoming requests from client
server.listen()

list_of_clients = []
nicknames = [] 

# defining questions and answers
questions = [
    "Who was the first woman to fly solo across the Atlantic Ocean? \n A. Bessie Coleman \n B. Amy Johnson \n C. Amelia Earhart \n D. Elinor Smith",
    "What species can live on both water and land? \n A. Birds \n B. Amphibians \n C. Reptiles \n D. Mammals",
    "What type of join is the human shoulder?  \n A. Ball-and-socket \n B. Hinge joint \n C. Pivot joint \n D. Saddle joint",
    "Which planet is closest to our sun? \n A. Venus \n B. Mercury \n C. Mars \n D. Earth",
    "How many continenets are there? \n A. 8 \n B. 5 \n C. 7 \n D. 6",
    "What type of bean is used for making miso? \n A. Lima Beans \n B. Miso Beans \n C. Chickpeas \n D. Soybeans",
    "What is the world's largest desert? \n A. Sahara \n B. Arabian Desert \n C. Gobi Desert \n D. Mojave Desert",
    "What is the mascot of the Walt Disney company? \n A. Disney \n B. Mickey Mouse \n C. Minnie Mouse \n D. Donald Duck"
]

answers = ['c', 'b', 'a', 'b', 'c', 'd', 'a', 'b']

print("Server has started...")

def clientthread(conn, nickname):
    score = 0
    print("clientthread is running")
    
    # sending clients instructions encoded with utf-8
    conn.send("Welcome to Random Fun Trivia!".encode('utf-8'))
    conn.send("Answer the questions that you receive. \n".encode('utf-8'))
    conn.send("Good luck and have fun! \n\n".encode('utf-8'))

    # saving returned index, question, and answer variables 
    index, question, answer = get_random_question_answer(conn)

    # loop to listen to any messages received from client
    while True:
        try:
            # receiving the message from client and decoding the encrypted message
            message = conn.recv(2048).decode('utf-8')
            name, correct_answer = message.split(':')

            try:
                name, correct_answer = message.split(':')
            except ValueError:
                print("received message isn't in expected format")

            print(f"received message from client: {correct_answer}")
            print(f"correct answer: {answer}")

            # checking if message is valid or not
            if message:
                # checking if the client's message matches with answer
                if correct_answer.lower() == answer:
                    score += 1
                    conn.send("Yes, that's the correct answer. Way to go! \n".encode('utf-8'))
                    conn.send(f"Your score is {score} \n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer. Better luck next time! \n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

# function to remove the client's connection from server after client has closed application
def remove(conn):
    if conn in list_of_clients:
        list_of_clients.remove(conn)

# removes question & answer at that particular index
def remove_question(random_index):
    questions.pop(random_index)
    answers.pop(random_index)

# removes client's nickname fro mthe list of nicknames
def remove_nickname():
    if nickname in nicknames:
        nicknames.remove(nickname)

def get_random_question_answer(conn):
    # getting a random index from question list
    random_index = random.randint(0, len(questions) - 1)
    random_question = questions[random_index] # getting a random question
    random_answer = answers[random_index] # getting a random answer
    conn.send(random_question.encode('utf-8')) # sending client the random question
    
    return random_index, random_question, random_answer
    
# loop to accpet all incoming connection requests from clients
while True:
    # conn is the socket object of the client (client socket) that is trying to connect to server
    # addr is the ip address + port number in a tuple format 
    conn, addr = server.accept() # accpeting the connection requests from clients

    conn.send('NICKNAME'.encode('utf-8')) # sending this message to client

    nickname = conn.recv(2048).decode('utf-8') # receiving user's nickname
    nicknames.append(nickname)
    print(nickname + " is connected!")

    list_of_clients.append(conn) # adding clients to list of clients

    new_thread = Thread(target=clientthread, args=(conn, nickname))
    new_thread.start() # starting the thread