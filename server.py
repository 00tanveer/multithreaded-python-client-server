# import socket programming library
import socket

# import thread module
from _thread import start_new_thread
import threading
import time

import subprocess

n = 0
count = 0
c = 0
print_lock = threading.Lock()
WINDOW_SIZE = 5

# thread function
def connection(c):
    while True:
        # data received from client
        data = c.recv(1024)
        global n
        global count
        if not data:
            print('Bye')
            break
        message = str(data.decode('ascii'))
        if n <= WINDOW_SIZE and message == 'run 1 matching':
            print('ACK - stashed match call')
            count = count + 1
            response = 'ACK - stashed match call'

            # send reponse to client
            c.send(response.encode('ascii'))

def timer():
    global n
    global count
    global c
    while True:
        n = n + 1
        time.sleep(1)
        print(n)
        if(n == WINDOW_SIZE):
            n = 0
            if(count > 0):
                response = 'ACK - ran matching routine'
                print('running matching routine')
                count = 0
                subprocess.call(['python', 'mongopython.py'])
                c.send(response.encode('ascii'))

def Main():
    global c
    host = ''

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 1234
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print('socket binded to port', port)

    # put the socket into listening mode
    s.listen(2)
    print('socket is listening')

    # start timer
    start_new_thread(timer, ())

    while True:
        # establish connection with client
        c, addr = s.accept()

        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(connection, (c,))

if __name__ == '__main__':
    Main()