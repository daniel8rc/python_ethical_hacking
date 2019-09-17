#!/usr/bin/python3

from socket import *
import threading
from termcolor import colored
import optparse


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
        setdefaulttimeout(1)

    def to_int(self, array_strings: list):
        """
        Convert array strings to array integers
        """
        return list(map(int, array_strings))

    def clean_multi_port(self, ports):
        ports = ports.replace(' ', '').replace('[', '').replace(']', '').split('-')
        
        ports = self.to_int(ports)

        if len(ports) != 2:
            raise("The structure of the ports isn't valid.")
        self.reverse = False
        if ports[0] > ports[1]:
            self.reverse = True
            ports[0], ports[1] = ports[1], ports[0]

        return ports

    def specific_port_scanner(self, port):
        sock = socket(AF_INET, SOCK_STREAM)
        
        if not sock.connect_ex((self.host, port)):
            print(colored("[+] Port %d/tcp is Open." % (port), 'green'))
        
        sock.close()
        # else:
        #     print("Port %d is close." % (port))

    def scann_multi_port(self):
        if self.ports:
            if len(self.ports) != 2:
                for p in self.ports:
                    t = Threads(self.specific_port_scanner, p)
                    t.run()

            elif self.reverse:
                for p in reversed(range(self.ports[0], self.ports[1])):
                    t = Threads(self.specific_port_scanner, p)
                    t.run()
                    
            else:
                for p in range(self.ports[0], self.ports[1]):
                    t = Threads(self.specific_port_scanner, p)
                    t.run()

            t.wait_threads()

    def show_host(self, host):
        try:

            target_ip = gethostbyname(host)
        except:
            print(colored( "Unknown Host %s " % (host)), 'grey')

        try:

            target_name = gethostbyaddr(host)
            print(colored("[+] Scan Results for: %s " % (target_name[0]), 'yellow'))
        except:
            print(colored("[+] Scan Results for: %s " % (target_ip), 'yellow'))

    def scann_ports(self):

        parser = optparse.OptionParser('Usage of program: ' + '-H <target host> -p <target port> -P [<init target ports>-<final target port]')
        parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
        parser.add_option('-p', dest='tgtPort', type='string', help='specify target ports separated by comma')
        parser.add_option('-P', dest='tgtPortRange', type='string', help='specify destination port range. Ex: -P [1-2] ')
        (options, args) = parser.parse_args()

        if (options.tgtHost == None):
            print(parser.usage)
            exit(0)
        if(options.tgtPort == None and options.tgtPortRange == None):
            print(parser.usage)
            exit(0)
        
        self.host = options.tgtHost
        self.show_host(self.host)

        if options.tgtPort:
            self.ports = self.to_int((options.tgtPort).replace(' ', '').split(','))
            self.scann_multi_port()

        if options.tgtPortRange:
            self.ports = self.clean_multi_port(options.tgtPortRange)
            self.scann_multi_port()
        
        print("Finished scann!")

    def run(self):
        self.scann_ports()

if __name__ == "__main__":
    scan = Scanner()
    scan.run()

