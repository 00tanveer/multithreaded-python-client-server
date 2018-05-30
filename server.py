# import socket programming library
import socket

# import thread module
from _thread import start_new_thread
import threading
import time

print_lock = threading.Lock()

# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        if not data:
            print('Bye')

            # lock released on exit
            print_lock.release()
            break

        # if a match-run signal, then run 1 mathcing
        message = str(data.decode('ascii'))
        if message == 'run 1 matching':
            print('running matching')
            time.sleep(2)
            response = 'finished running 1 matching'
            print(response)

            # send finish reponse to client
            c.send(response.encode('ascii'))

    # connection closed
    c.close()

def Main():
    host = ''

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print('socket binded to post', port)
    
    # put the socekt into listening mode
    s.listen(5)
    print('socket is listening')

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