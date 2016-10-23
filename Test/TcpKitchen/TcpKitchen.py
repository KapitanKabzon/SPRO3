# Sets up python server and client in the hotel kitchen using tcp protocol
# h is communication between the kitchen the hotel customer
# p is communication between the kitchen and the Raspberry Pi

import socket

TCP_IP_KIT = '10.0.1.15'  # IP on which the kitchen server is listening
TCP_IP_PI = '10.0.1.15'  # IP on which the Raspberry Pi server is listening
TCP_PORT_KIT = 5005  # Port for the Kitchen
TCP_PORT_PI = 13000  # Port for the Raspberry Pi

BUFFER_SIZE = 50  # maximum characters coming for the room number 

h = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
h.bind((TCP_IP_KIT, TCP_PORT_KIT))
h.listen(1)

while 1:
	conn, addr = h.accept()
	print("Connection address:", addr)

	while 1:
		# gets order information from hotel customer
		order = conn.recv(BUFFER_SIZE)
		if not order:
			break
		print("Order placed:", order.decode())  # prints the order
		tosend = "true"
		conn.send(tosend.encode())  # sends confirmation to client
		
		# gets room number information from hotel customer
		conn, addr = h.accept()
		roomnr = conn.recv(BUFFER_SIZE)
		if not roomnr:
			break
		print("Room number:", roomnr.decode())
		
		# sends room number information to Raspberry Pi
		p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			p.connect((TCP_IP_PI, TCP_PORT_PI))
			p.send(roomnr)
			check = p.recv(BUFFER_SIZE)
			p.close()
		except socket.error:
			check = "false"
			check = check.encode()
			print("Failure to communicate with Automated Bellhop")

		conn.send(check)

	conn.close()  # closes the connection to the client
		
