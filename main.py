# This is a sample Python script.

import socket
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
exit = False


def rxThread(portNum):
    global exit



    # Generate a UDP socket
    rxSocket = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP

    # Bind to any available address on port *portNum*
    rxSocket.bind(("", portNum))

    # Prevent the socket from blocking until it receives all the data it wants
    # Note: Instead of blocking, it will throw a socket.error exception if it
    # doesn't get any data

    rxSocket.setblocking(0)

    print("RX: Receiving data on UDP port " + str(portNum))
    print("")

    count = 0

    Ax = []
    Ay = []
    Az = []
    print("Initialization")
    while (count < 10):
        try:
            # Attempt to receive up to 1024 bytes of data
            data, addr = rxSocket.recvfrom(1024)
            # Echo the data back to the sender
            # rxSocket.sendto(str(data),addr)
            strData = str(data).replace('\'', '').replace('b', '').replace('\\r\\n', '')
            splitData = strData.split(",")
            print(strData)
            #print(len(strData))
            if (len(strData) > 10):

                Ax.append(float(splitData[0]))
                Ay.append(float(splitData[1]))
                Az.append(float(splitData[2]))


                #print(Ax)

                count = count+1

        except:
            pass

    Axm = np.mean(Ax)
    Aym = np.mean(Ay)
    Azm = np.mean(Az)
    print("Mean values")
    print(Axm)
    print(Aym)
    print(Azm)

    A = []
    Ax = []
    Ay = []
    Az = []
    x = []
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    line1, = ax.plot(x, Ax, 'b-')

    plt.xlabel("Time")
    plt.ylabel("Acceleration")
    plt.title('Vibrations')


    print("Main Loop")
    while not exit:
        try:
            # Attempt to receive up to 1024 bytes of data
            data, addr = rxSocket.recvfrom(1024)
            # Echo the data back to the sender
            # rxSocket.sendto(str(data),addr)
            strData = str(data).replace('\'', '').replace('b', '').replace('\\r\\n', '')
            splitData = strData.split(",")
            print(strData)

            #Ax.append(float(splitData[0])-Axm)
            #Ay.append(float(splitData[1])-Aym)
            #Az.append(float(splitData[2])-Azm)
            A.append(((float(splitData[0])-Axm)**2+(float(splitData[1])-Aym)**2+(float(splitData[2])-Azm)**2)**0.5)

            count = count+1
            x.append(datetime.now())
            #x.append(count)


            if (len(A) > 100):
                #Ax.pop(0)
                #Ay.pop(0)
                #Az.pop(0)
                A.pop(0)
                x.pop(0)

            #print(A)

            plt.clf()
            plt.plot(x, A)
            plt.ylim([0, 5])
            plt.xlabel("Time")
            plt.ylabel("Acceleration")
            plt.title('Vibrations')
            plt.draw()
            plt.show()
            plt.pause(0.005)

        except:
            pass
# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    rxThread(60575)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
