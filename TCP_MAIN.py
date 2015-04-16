#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket, sys, re, random,TCP_functions

end = b'^'      #used for recvVar (where the return value will have varying lengths)
chat = b'#'     #used to indicate back and forth communication from server called methods and the user

#--------------------------------------------------

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received' ' %d bytes before the socket closed' % (length, len(data)))
        data += more
    return data




#--------------------------------------------------

def recvVar(sock):
    data = b''
    more = b''
    while (more != b'^'):
        more = sock.recv(1)
        if (more != b'^'):
            data += more

    return data

#--------------------------------------------------

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:





        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print(' Socket name:', sc.getsockname())
        print(' Socket peer:', sc.getpeername())



        interacting = True
        while (interacting):


            choiceEnc = recvall(sc,1)
            choice = choiceEnc.decode('ascii')
            #print(choice)

            if int(choice) == 1:
                message = TCP_functions.addNewEmployee(sc)
                while (message == "redo"):
                    message = TCP_functions.addNewEmployee(sc)

            elif int(choice) == 2:
                message = TCP_functions.searchForEmployee(sc)
                while (message == "redo"):
                    message = TCP_functions.searchForEmployee(sc)

            elif int(choice) == 3:
                message = TCP_functions.removeEmployee(sc)
                while (message == "redo"):
                    message = TCP_functions.removeEmployee(sc)

            elif int(choice) == 4:
                message = TCP_functions.displayDatabase()

            elif int(choice) == 5:
                message = "\nGoodbye\n--\n"
                #ends program (QUIT)
            else:
                message = "That is not an option, Please try again."

            message += "^"
            sc.sendall(bytes(message, encoding='ascii'))

            if(message == "\nGoodbye\n--\n^"):
                interacting = False
                sc.close()
                print("SOCKET CLOSED\n")









        '''message = recvall(sc, 16)
        print(' Incoming sixteen-octet message:', repr(message))
        sc.sendall(b'Farewell, client')
        sc.close()
        print(' Reply sent, socket closed')'''



#--------------------------------------------------

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())

 
    run = True;

    while (run):



        choice = TCP_functions.mainMenu()
        print()
        #print(choice)
        #print(bytes(choice, encoding = 'ascii'))

        sock.sendall(bytes(choice, encoding = 'ascii'))

        replyEnc = recvVar(sock)
        reply = replyEnc.decode('ascii')

        #print(reply)
        #print(reply[-1:])
        if(reply[-1:] != "#"):
            print(reply)
        else:    
            while(reply[-1:] == "#"):
                print(reply.rstrip("#"))
                data = input()
                data += "^"
                sock.sendall(data.encode('ascii'))
                replyEnc = recvVar(sock)
                reply = replyEnc.decode('ascii')

        if(reply == "\nGoodbye\n--\n"):
            run = False
            sock.close()
            print("SOCKET CLOSED")




'''
    sock.sendall(b'Hi there, server')
    reply = recvall(sock, 16)
    print('The server said', repr(reply))
    sock.close()'''





#--------------------------------------------------

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;' ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=2015, help='TCP port (default 2015)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)





