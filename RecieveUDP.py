#!/usr/bin/python3

import socket
from threading import Thread
import threading 
from time import sleep
import sys
import serial
from datetime import datetime

exit = False

def serialReadThread(ser):
    global exit
    
    portNum = 60575
    
    txSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    # Serial Connection Setup
    
    
    while not exit:
        reading = ser.readline()
        print(reading)
        #file.write(reading.decode('UTF-8'))
        txSocket.sendto(reading,("172.17.11.193",portNum))
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line)
#             txSocket.sendto(line.encode('utf-8'),("172.17.8.139",portNum))
#             ser.flush()
    

def rxThread(portNum,ser):
    global exit
    
    #Generate a UDP socket
    rxSocket = socket.socket(socket.AF_INET, #Internet
                             socket.SOCK_DGRAM) #UDP
                             
    #Bind to any available address on port *portNum*
    rxSocket.bind(("",portNum))
    
    #Prevent the socket from blocking until it receives all the data it wants
    #Note: Instead of blocking, it will throw a socket.error exception if it
    #doesn't get any data
    
    rxSocket.setblocking(0)
    
    print("RX: Receiving data on UDP port " + str(portNum))
    print("")
    
    while not exit:
        try:
            #Attempt to receive up to 1024 bytes of data
            data,addr = rxSocket.recvfrom(1024) 
            #Echo the data back to the sender
            #rxSocket.sendto(str(data),addr)
            strData = str(data)
            print(strData)
            if strData == "b\'start\'":
                now = datetime.now().strftime("%d%H%M%S.csv")
                print(now)
                ser.write(("start\n"+now).encode('utf-8'))
                #ser.write(("start\n"+"Test.txt").encode('utf-8'))
                print("**************************************************************************************************************************")
            elif strData == "b\'end\'":
                ser.write(("end\n").encode('utf-8'))
                print("**************************************************************************************************************************")
                

        except socket.error:
            #If no data is received, you get here, but it's not an error
            #Ignore and continue
            pass
        except:
            
            print("Error")
        sleep(.01)
    
def txThread(portNum):
    global exit
    
    
def main(args):    
    global exit
    print("Read Vibration Sensor Data")
    print("Press Ctrl+C to exit")
    print("")
    
    #file = open('Failed.py', 'a')
    portNum = 64126
   
    # Serial Connection Setup
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.05)
    except:
        ser = serial.Serial('/dev/ttyACM1', 115200, timeout=0.05)
    ser.flush()
    
    udpRxThreadHandle = Thread(target=rxThread,args=(portNum,ser))    
    udpRxThreadHandle.start()
        
    sleep(.1)
    
    #Generate a transmit socket object
    txSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    
    #Do not block when looking for received data (see above note)
    txSocket.setblocking(0) 
   
    print("Transmitting to 172.17.8.193 port " + str(portNum))
    
    x = threading.Thread(target=serialReadThread, args=(ser,))
    x.start()
    
    
    
    while True:
        
#         if ser.in_waiting > 0:
#             line = ser.readline().decode('utf-8').rstrip()
#             print(line)
#             txSocket.sendto(line.encode('utf-8'),("172.17.8.139",portNum))
#             ser.flush()
        
        #ser.write(b"Hello from Raspberry Pi!\n")
        try:
             #Retrieve input data 
            txChar = raw_input("TX: ")
            
            #Transmit data to the local server on the agreed-upon port
            txSocket.sendto(txChar,("172.17.8.139",portNum))
            
            #Sleep to allow the other thread to process the data
            sleep(.2)
            
            #Attempt to receive the echo from the server
            data, addr = txSocket.recvfrom(1024)
            
            print("RX: " + str(data))

        except KeyboardInterrupt:
            exit = True
            #file.close()
            print("Received Ctrl+C... initiating exit")
            break
        except:    
            #If no data is received you end up here, but you can ignore
            #the error and continue
            pass   
         
    udpRxThreadHandle.join()
        
    return

if __name__=="__main__":
    main(sys.argv[1:0])