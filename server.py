#####################################################################################
#              [198 340 Computer Networks] Project Switch Simulator                 #
#  By Mr.Athibet Prawane 593040685-3 and Mr.Chalermchai Viriyamanatham 593040658-6  #
#####################################################################################
import socket  # call module socket to create link to connect the server
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # call tcp object
ip_server = str(socket.gethostbyname(socket.gethostname()))
print('====================>>> Switch <<<====================\n')
port = int(input('Please setting port of server: '))  # setting port of server

answer = input('Start run server [y/n]: ')  # enter y to run server
if answer.lower() != 'y':
    print('You did not indicate approval')
    exit(1)

s.bind((ip_server, port))  # connect tcp object
s.listen()  # assume amount of client

print('\nServer ready...')
print('Ip Address of the server is: %s' % ip_server)
print('\nYou will need to fill in the server port and ip address\non the client side to match the server side.')
print('-------------------------------------------------------\n')
# waiting for client connected

table = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clients = {}

# information command
command_help = ('\nCOMMAND\t\t\t\t\tDESCRIPTION\nping <desination IP address>\t\tTest connection with destination.\n'
                + 'quit()\t\t\t\t\tTo end your session\n'
                + '\nFor show a specific command again, type HELP command-name'
                + '\n-------------------------------------------------------------------------\n')

port_interface = ['f0/1', 'f1/1', 'f2/1', 'f3/1', 'f4/1',
                  'f5/1', 'f6/1', 'f7/1', 'f8/1', 'f9/1', 'f10/1']
ip_address = [None]*10
mac_address = [None]*10
i = 0


def checkPort(name):
    pos = [i for i, n in enumerate(ip_address) if n == name]
    return port_interface[pos[-1]]


def handleClient(client, uname):
    keys = clients.keys()
    help = command_help
    clientConnected = True
    while clientConnected:  # waiting connected by client when clientConnected is 'True'
        try:
            # read data ascii to string type
            data = client.recv(1024).decode('ascii')
            found = False
            if 'help' in data:
                client.send(help.encode('ascii'))
            elif 'quit()' in data:
                response = 'Stopping Session and exiting...'
                client.send(response.encode('ascii'))
                clients.pop(uname)
                print('status: ' + uname + ' interface port ' + port_interface[ip_address.index(uname)]
                      + ' has been disconnected from the server')
                clientConnected = False
            else:
                for name in keys:
                    if('ping ' + name) in data:
                        msg = ('Ping for ' + name + ' is: Complete!')
                        client.send(msg.encode('ascii'))
                        des = (
                            name + ',' + mac_address[ip_address.index(name)] + ',' + checkPort(name))
                        src = (
                            uname + ',' + mac_address[ip_address.index(uname)] + ',' + checkPort(uname))
                        table.sendto(src.encode('ascii'), ('127.0.0.1', port))
                        table.sendto(des.encode('ascii'), ('127.0.0.1', port))
                        found = True
                if(not found):
                    msg_fail = ('Please try again.')
                    client.send(msg_fail.encode('ascii'))
        except:
            clients.pop(uname)
            print('status: ' + uname + ' interface port ' +
                  port_interface[ip_address.index(uname)] + ' has been disconnected from the server')
            clientConnected = False


while True:  # server is running for receive any data from client
    client, address = s.accept()  # receive data frome client ip and port
    ip_client2 = client.recv(1024).decode('ascii')
    ip_client3 = ip_client2.split(',')
    ip_client = ip_client3[0]
    mac_client = ip_client3[1]
    # read data ascii to string type
    print('status: ' + str(ip_client) + ' interface port ' +
          str(port_interface[i]) + ' connected to the server')
    ip_address[i] = str(ip_client)
    mac_address[i] = str(mac_client)
    start_connect = (
        '\nYou have connected to the server, and your port interface is: ' + port_interface[i] + '\n' + command_help)
    # encode string to ascii code and send the data to client
    client.send(start_connect.encode('ascii'))
    i += 1

    if(client not in clients):
        clients[ip_client] = client
        threading.Thread(target=handleClient, args=(
            client, ip_client, )).start()
