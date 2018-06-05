# import socket programming library
import socket

# import thread module
from _thread import start_new_thread
import threading
import time

import subprocess

n = 0
count = 0
print_lock = threading.Lock()
WINDOW_SIZE = 5

# thread function
def threaded(c):
    while True:
        # data received from client
        data = c.recv(1024)
        global n
        global count
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break
        if n < WINDOW_SIZE and count == 1:
            response = 'recently ran 1 matching'
            print(response)
            # send reponse to client
            c.send(response.encode('ascii'))
            c.close()
            print_lock.release()
            break
        # if a match-run signal, then run 1 mathcing
        message = str(data.decode('ascii'))
        if message == 'run 1 matching':
            print('running matching')
            subprocess.call(['python', 'mongopython.py'])
            count = count + 1
            response = 'finished running 1 matching'
            print(response)

            # send finish reponse to client
            c.send(response.encode('ascii'))
            c.close()
            print_lock.release()
            break
    # connection closed

def timer():
    global n
    global count
    while True:
        n = n + 1
        time.sleep(1)
        if(n == WINDOW_SIZE):
            n = 0

def Main():
    host = ''

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print('socket binded to port', port)

    # put the socket into listening mode
    s.listen(2)
    print('socket is listening')

    # start timer
    start_new_thread(timer, ())

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client, it hogs the connection
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()

if __name__ == '__main__':
    Main()