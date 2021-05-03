# This is a sample Python script.

import socket

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

    while not exit:
        try:
            # Attempt to receive up to 1024 bytes of data
            data, addr = rxSocket.recvfrom(1024)
            # Echo the data back to the sender
            # rxSocket.sendto(str(data),addr)
            strData = str(data)
            print(strData)
        except:
            pass
# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    rxThread(60575)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
