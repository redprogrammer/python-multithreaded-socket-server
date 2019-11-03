#!/bin/env python3

import sys
import socket
import os
from base64 import b64encode, b64decode
import select
import readline
import logging

def read_pp():
    host = socket.gethostname()
    try:
        # username = sys.argv[1]
        # password = sys.argv[2]
        host = sys.argv[1]
        # return username, password, host
        return host
    except IndexError:
        print("Please give: username, password & hostnamed in this order",
        "Example: python client.py user1 pass 10.0.0.1")
        sys.exit(1)

# username, password, host = read_pp()
host = read_pp()

class initCom():
    def __init__(self, host, port=55557, username=None, password=None, BUFFER_SIZE=8192):
        self.port = port
        self.host = host
        self.BUFFER_SIZE = BUFFER_SIZE
        self.tcpClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_state(True)
        self.error_ct = 0
        self.run()

    def die(self, *args):
        '''Fata error handling function for
        issuing none, one or many warnings before exiting
        '''
        for msg in args:
            print(msg)
        self.stop_socket(True)

    def socket_state(self, state):
        self.running_state = state

    def stop_socket(self, stop=False):
        if stop and self.running_state:
            print("INFO: Socket client will exit")
            self.socket_state(False)
            self.close_socket()
        elif stop and not self.running_state:
            print("INFO: Waiting for all active transactions to complete.")

        self.report()

    def close_socket(self):
        self.tcpClient.shutdown(socket.SHUT_RDWR)
        self.tcpClient.close()

    def com_drop(self):
        print("COMDROP")
        self.tcpClient.setblocking(False)
        self.com_drop_status = True
        while True:
            clear_socket = select.select([self.tcpClient], [], [], 2)
            if clear_socket[0]:
                try:
                    self.dump_socket_data = self.read_socket()
                    if self.dump_socket_data == '' or self.dump_socket_data == ' ':
                        break
                except:
                    break
            else:
                break

        self.tcpClient.setblocking(True)

    def report(self):
        if self.running_state:
            print(
                "INFO: Socket Client is running:")
        else:
            print("INFO: Socket Client has stopped")

    def message_com(self, data, buffer=8192):
        if data == '00xSOT00x':
            self.tcpClient.sendall(b64encode('00xSOT00x'.encode('utf-8')))
            return True
        
        elif data == '00xEOT00x':
            self.tcpClient.sendall(b64encode('00xEOT00x'.encode('utf-8')))
            return False
        
        elif data == '01xSOM01x':
            self.tcpClient.sendall(b64encode('01xSOM01x'.encode('utf-8')))

            self.tcpClient.setblocking(False)
            socRDY = select.select([self.tcpClient], [], [], 2)
            if socRDY[0]:
                data = self.read_socket()
                print(data)
            else:
                self.tcpClient.sendall(b64encode('01xROM01x'.encode('utf-8')))
                print("INFO: Timed out waiting for a response from server.")
                return False

            self.tcpClient.setblocking(True)

            self.tcpClient.sendall(b64encode('01xROM01x'.encode('utf-8')))
            return True

        elif data == '01xEOM01x':
            self.tcpClient.sendall(b64encode('01xEOM01x'.encode('utf-8')))
            return True

        elif data == '00xEOT00x':
            self.tcpClient.sendall(b64encode('00xEOT00x'.encode('utf-8')))
            return True

        elif data == '009x0DT000x0':
            self.com_drop()
            return False
        else:
            self.tcpClient.sendall(b64encode('009x0SET000x0'.encode('utf-8')))
            self.com_drop()
            if self.error_ct >=20:
                self.stop_socket(True)
                return False
            return False
        
    def send_request(self, request):
        self.tcpClient.sendall(b64encode(request.encode('utf-8')))

        while True:
            self.srvdata = self.read_socket()
            if not self.message_com(self.srvdata):
                break

    def init_sync(self):
        self.srvdata = self.read_socket()
        if self.srvdata != '00xSOS00xHELLOx00':
            self.die("Communication error")
        else:
            self.tcpClient.sendall(b64encode('00xSOS00xHELLOx00'.encode('utf-8')))

    def completer(self, text, state):
        self.options = sorted(
            [
                "system",
                "ls",
                "pwd",
                "cwd",
                "exit",
                "quit",
                "clear",
            ]
        )
        response = None
        if state == 0:
            if text:
                self.matches = [s 
                                for s in self.options
                                if s and s.startswith(text)]

            else:
                self.matches = self.options[:]
        
        try:
            response = self.matches[state]
        except IndexError:
            response = None

        return response

    def decode_data(self, data):
        return b64decode(data).decode('utf-8')

    def read_socket(self, buffer=8192):
        data = self.tcpClient.recv(buffer)
        return self.decode_data(data)

    def run(self):
        print("\n------------ RemoteCLI ------------")
        print("\n\t* Socket Client *\n")
        print("-----------------------------------\n")
        
        self.tcpClient.connect((self.host, (self.port)))
        self.init_sync()
        
        readline.set_completer(self.completer)
        readline.parse_and_bind('tab: complete')

        while self.running_state:
            try:
                self.error_ct = 0
                self.toserver = ''
                self.toserver = input("Input :: <= ")
            except KeyboardInterrupt:
                self.stop_socket(True)
                break
 
            if self.toserver in ['Exit', 'Quit', 'exit', 'quit', 'q', 'bye', 'Bye']:
                self.send_request(self.toserver)
                break

            if self.toserver == '' or self.toserver is None or not self.toserver:
                continue
            elif self.toserver == 'clear':
                os.system("clear")
                continue
        
            self.send_request(self.toserver)

if __name__ == "__main__":
    try:
        cli = initCom(host=sys.argv[1])
    except KeyboardInterrupt:
        cli.stop_socket(True)