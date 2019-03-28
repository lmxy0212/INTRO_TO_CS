f = open("train.csv", "r+")
out = open("new.csv","w")
# line = f.readline()
# print(line)
# print("hi")
i = 0
for line in f:
    # print("1",line)
    line = line.strip("\n")
    lst = line.split(",")
    if i == 0:
        newline =line + ",if survived,if female,if old,if Cabin type,if embark s"
        f.readline()
        print(line,file=out)
    else:
        newline = f.readline().strip("\n")
        print(newline, end="", file=out)
        if lst[1] == "0":
            print(",n",end="",file=out)
        elif lst[1] == "1":
            print(",y", end="",file=out)
        else:
            print(",", end="", file=out)

        if lst[5] == "female":
            print(",y",end="",file=out)
        elif lst[5] == "male":
            print(",n", end="",file=out)
        else:
            print(",", end="", file=out)

        if lst[6] == "":
            print(",", end="", file=out)
        else:
            if float(lst[6])>50:
                print(",y",end="",file=out)
            elif float(lst[6])<50:
                print(",n", end="",file=out)


        if lst[-2] == "":
            print(",n",end="",file=out)
        else:
            print(",y", end="", file=out)

        if lst[-1] == "S":
            print(",y",end="",file=out)
        else:
            print(",n", end="", file=out)
        print(file=out)

        print(lst)
    i+=1
print("hi",f.readline())

outfile = open("new.csv", "r")
for line in outfile:
    print(1)
    print(line.strip())
    # sock.send(line.strip().encode())
# f.close()