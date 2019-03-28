import socket
import sys

# create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connection info
server_address = ('chalbroker.cs1122.engineering.nyu.edu', 3120)
# connect to the server
sock.connect(server_address)

try:
    # receive data from the server
    print(sock.recv(1024))
    # tell the server who you are
    sock.send("ml5719\n".encode()) # your net id

    # receive confirmation from the server
    print(sock.recv(1024))
    # receive the challenge
    data = sock.recv(1024).decode("utf8")
    print(data)
    #
	# Solve the given challenge and return the answer as specified by the instructions
	#

    s= data.split("\n")[1]
    lst = [int(s.split(", ")[i]) for i in range(len(s.split(", ")))]
    # print(lst)
    for j in range(len(lst) - 1, 0, -1):
        for i in range(j):
            if lst[i] > lst[i + 1]:
                lst[i],lst[i+1]=lst[i+1],lst[i]
    answer_str=" ".join([str(i) for i in lst])+"\n"

    #  send the server your answer
    sock.send(answer_str.encode())
    print(answer_str)
    print(sock.recv(1024))


finally:
    # close the connection
    sock.close()
