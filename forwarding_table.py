#####################################################################################
#              [198 340 Computer Networks] Project Switch Simulator                 #
#  By Mr.Athibet Prawane 593040685-3 and Mr.Chalermchai Viriyamanatham 593040658-6  #
#####################################################################################
import socket
import threading
import os
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('==================>>> Forwarding table <<<==================\n')
port = int(input('Please enter port of server: '))  # enter port of server

ip_localhost = '127.0.0.1'

s.bind((ip_localhost, port))

def header():
    print('\n\t\t\tForwarding Table')
    print('\t=============================================')
    print('\t Mac Address\t\t\t\tPort')
    print('\t=============================================')

os.system('cls')
header()

macTable = []
clientRunning = True
stop = True

def removeTable():
    global macTable
    if len(macTable) > 0:
        macTable.remove(macTable[0])
        showTable(macTable)

def receiveMsg(sock):  # for check server active
    global stop
    serverDown = False
    while clientRunning and (not serverDown):
        try:
            msg, addr = sock.recvfrom(1024)
            msg = str(msg)[2:len(str(msg))-1]
            ip, mac, port = msg.split(',')
            subAddr = (ip, mac, port)

            if subAddr not in macTable:
                macTable.append(subAddr)
            showTable(macTable)
        except:
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            serverDown = True

threading.Thread(target=receiveMsg, args=(s,)).start()

def showTable(macTable):
    os.system('cls')
    header()
    for i in macTable:
        print('\t' + i[1] + '\t\t\t' + i[2])