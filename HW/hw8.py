import socket
import sys

# create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connection info
server_address = ('chalbroker.cs1122.engineering.nyu.edu', 3545)
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
    f = open("train.csv", "r+")
    out = open("new.csv", "w")
    # line = f.readline()
    # print(line)
    # print("hi")
    i = 0
    for line in f:
        if line == "\n":
            line.strip()
        line = line.strip("\n")
        lst = line.split(",")
        if i == 0:
            newline = line + ",if survived,if female,if old,if Cabin type,if embark s"
            f.readline()
            print(newline, file=out)
        else:
            newline = ",".join(lst)
            print(newline, end="", file=out)
            if lst[1] == "0":
                print(",n", end="", file=out)
            elif lst[1] == "1":
                print(",y", end="", file=out)
            else:
                print(",None", end="", file=out)

            if lst[5] == "female":
                print(",y", end="", file=out)
            elif lst[5] == "male":
                print(",n", end="", file=out)
            else:
                print(",None", end="", file=out)

            if lst[6] == "":
                print(",None", end="", file=out)
            else:
                if float(lst[6]) > 50:
                    print(",y", end="", file=out)
                elif float(lst[6]) < 50:
                    print(",n", end="", file=out)

            if lst[-2] == "":
                print(",n", end="", file=out)
            else:
                print(",y", end="", file=out)

            if lst[-1] == "S":
                print(",y", end="", file=out)
            else:
                print(",n", end="", file=out)

            print(file=out)
            # print(lst)
        i += 1
    print("...x",end = "",file = out )
    f.close()
    out.close()

    # send the server your answer
    outfile = open("new.csv", "r")
    for line in outfile:
        print(line.strip())
        sock.send((line.strip()+"\n").encode())
        # print(sock.recv(1024))

    outfile.close()
    print("recv->",sock.recv(1024))
    print("done")


finally:
    # close the connection
    sock.close()
