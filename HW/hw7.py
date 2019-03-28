import socket
import random
import string
import hashlib
import sys

# create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connection info
server_address = ('chalbroker.cs1122.engineering.nyu.edu', 3543)
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
    four_digits = s.split()[-1][-4:]
    print(four_digits)

    guess = ""
    for i in range(4):
        guess += random.choice(string.ascii_lowercase + string.ascii_uppercase)
    # print(guess)
    m = hashlib.md5(guess.encode('utf-8')).hexdigest()[-4:]
    # m.update(guess)

    while m != four_digits:
        guess = ""
        for i in range(4):
            guess += random.choice(string.ascii_lowercase + string.ascii_uppercase)
        # print(guess)
        m = hashlib.md5(guess.encode('utf-8')).hexdigest()[-4:]

    guess+='\n'
    sock.send(guess.encode())
    print(guess)
    print(m)
    # print(four_digits)
    print(hashlib.md5(guess.encode('utf-8')).hexdigest())
    print(sock.recv(1024))
    print(sock.recv(1024))

finally:
    # close the connection
    sock.close()
