# sets up python server on the raspberry pi using tcp protocol

import socket

TCP_IP = '10.0.1.1' # (currently local) IP
TCP_PORT = 13000 # tcp port for Raspberry Pi
BUFFER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while 1:
    conn, addr = s.accept()
    print("Connection address:", addr)

    while 1:
        roomnr = conn.recv(BUFFER_SIZE)
        if not roomnr: break
        print("Room number:", roomnr.decode()) # prints the room number
        tosend = "On our way!"
        conn.send(tosend.encode()) # sends confirmation to client

conn.close() # closes the connection