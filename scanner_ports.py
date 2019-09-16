#!/usr/bin/python3

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "192.168.1.138"
port = 443

class Scanner:
    def __init__(self, host):
        self.host = host

    def specific_port_scanner(self, port):
        if sock.connect_ex((host, port)):
            print("Port %d is closed." % (port))
        else:
            print("Port %d is open." % (port))


if __name__ == "__main__":
    scan = Scanner(host)
    scan.specific_port_scanner(port)
