#####################################################################################
#              [198 340 Computer Networks] Project Switch Simulator                 #
#  By Mr.Athibet Prawane 593040685-3 and Mr.Chalermchai Viriyamanatham 593040658-6  #
#####################################################################################
import socket
import threading
import sys
import re
from uuid import getnode
# getting mac address
original_mac_address = getnode()
hex_mac_address = str(
    ":".join(re.findall('..', '%012x' % original_mac_address)))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('=============================>>> Client <<<=============================\n')
port = int(input('Please enter port of server: '))  # enter port of server
# port = 6060

ip = input('Enter the IP address of server: ')  # enter ip address of server
# ip = '10.61.239.138'

answer = input('Connect to server [y/n]: ')  # enter y to connect server
if answer.lower() != 'y':
    print('You did not indicate approval')
    exit(1)

# ip_client = str(socket.gethostbyname(socket.gethostname())) # call ip address
ip_client = '10.0.0.11'
print('IP Address is: ' + ip_client)

data = str(ip_client + ',' + hex_mac_address)

s.connect((ip, port))
s.send(data.encode('ascii'))  # send data to server and encode string to ascii

clientRunning = True


def receiveMsg(sock):  # for check server active
    serverDown = False
    while clientRunning and (not serverDown):
        try:
            msg = sock.recv(1024).decode('ascii')
            print(msg)
        except:
            print('Server is Down. You are now Disconnected. Press enter to exit...')
            serverDown = True


threading.Thread(target=receiveMsg, args=(s,)).start()

while clientRunning:
    tempMsg = input()
    msg = tempMsg
    if 'quit()' in msg:
        clientRunning = False
        s.send('quit()'.encode('ascii'))
    else:
        s.send(msg.encode('ascii'))
