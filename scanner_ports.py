#!/usr/bin/python3

import socket
import threading
from termcolor import colored


socket.setdefaulttimeout(2)


class Threads:
    def __init__(self, func, params):
        self.func = func
        self.params = params
        self.threads = []

    def wait_threads(self):
        """
        Wait for all threads to complete.
        """
        for t in self.threads:
            t.join()
        print("Finished scann")

    def execute_thread(self, args):
        
        if type(self.params)== int:
            thread = threading.Thread(target=self.func, args=(args,))
        else:
            thread = threading.Thread(target=self.func, args=args)

        # Start new Threads
        thread.start()
        # Add threads to thread list
        self.threads.append(thread)

    def run(self):
        self.execute_thread(self.params)


        
class Scanner:
    def __init__(self):
        self.ports = ''
        self.port = ''
        self.host = ''
        self.reverse = False

    def clean_multi_port(self):
        ports = self.ports.replace(' ', '').replace('[', '').replace(']', '').split('-')
        # To integer
        ports = list(map(int, ports))

        if len(ports) != 2:
            raise("The structure of the ports isn't valid.")
        self.reverse = False
        if ports[0] > ports[1]:
            self.reverse = True
            ports[0], ports[1] = ports[1], ports[0]

        return ports

    def specific_port_scanner(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        if not sock.connect_ex((self.host, port)):
            print(colored("[+] Port %d is open." % (port), 'green'))
        # else:
        #     print("Port %d is close." % (port))

    def scann_multi_port(self):
        if self.ports:
            if self.reverse:
                for p in reversed(range(self.ports[0], self.ports[1])):
                    t = Threads(self.specific_port_scanner, p)
                    t.run()
                    
            else:
                for p in range(self.ports[0], self.ports[1]):
                    t = Threads(self.specific_port_scanner, p)
                    t.run()

            t.wait_threads()
                
    def scann_ports(self):
        self.host = str(input("[*] Enter The Host to Scan: "))
        multiple_port = bool(
            (input("[*] Do you want to scanning multi-port? [Yy or Nn]: ")).lower() == 'y'
        )
        if not multiple_port:
            self.port = int(input("[*] Enter The Port to Scan: "))
            self.specific_port_scanner(self.port)
        else:
            self.ports = str(input("[*] Enter The Ports to Scan: [InitPort-Finalport]: "))
            self.ports = self.clean_multi_port()
            self.scann_multi_port()


    def run(self):
        self.scann_ports()

if __name__ == "__main__":
    scan = Scanner()
    scan.run()

