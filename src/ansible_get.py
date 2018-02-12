#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

from time import gmtime, strftime
from urlparse import urlparse, parse_qs

import subprocess, os

PORT_NUMBER = 8085

def ansible_playbook_run(playbook, host, name):
    print("executing playbook " + playbook + " on host " + host)
    fd = open('hosts', 'w')
    fd.write("[HOST]\n")
    fd.write(host)
    fd.write("\n")
    fd.close()
    bash_command = 'ansible-playbook playbook/' + playbook + '.yaml --inventory-file=hosts'
    output = open('log/' + name + '.log', 'w')
    process = subprocess.Popen(bash_command.split(), stdout=output)
    process.communicate()
    output.close()
    return 1

#This class will handles any incoming request 
class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        print(self.path)
        if self.path.startswith("/get_playbook"):
            parameters = parse_qs(urlparse(self.path).query)
            #Playbook name
            playbook = parameters['playbook'][0]
            #Name of the host (will be used in logs)
            name = parameters['name'][0]
            ansible_playbook_run(playbook, self.client_address[0], name);
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("playbook " + playbook + " started at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        else :
            self.send_response(403)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write("403 FORBIDDEN")
        return

try:
    #create folders if they don't exist
    if not os.path.exists("log"):
        os.makedirs("log")
        
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print('Started httpserver on port ')
    print(PORT_NUMBER)

    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()
