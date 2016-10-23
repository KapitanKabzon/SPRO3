# Sets up python server on the Raspberry Pi using tcp protocol
# k is communication between the Raspberry Pi and the kitchen

import socket

TCP_IP_PI = '10.0.1.15'  # IP that the Raspberry Pi is listening on
TCP_PORT_PI = 13000  # Port for the Raspberry Pi

BUFFER_SIZE = 50

k = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
k.bind((TCP_IP_PI, TCP_PORT_PI))
k.listen(1)

while 1:
	conn, (host,port) = k.accept()
	print("Connection address:", host)

	while 1:
		roomnr = conn.recv(BUFFER_SIZE)
		if not roomnr:
			break
		print("Room number:", roomnr.decode())  # prints the room number
		check = "true"
		conn.send(check.encode())  # sends confirmation to client
	
	conn.close()  # closes the connection to the client