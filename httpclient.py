#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Copyright 2017 Chenrui Lei
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

    def __str__(self):
        return str(self.code) + ' ' + str(self.body)

class HTTPClient(object):
    def get_host_path_port(self,url):
        if not len(url)>0:
            raise()

        # get host
        if ('://' in url):
            url_parts = url.split('://')
            url_parts = url_parts[1]
        else:
            url_parts = url

        if ('/' in url_parts):
            url_parts_host = url_parts.split('/')
            url_parts = url_parts_host
        elif (':' in url_parts):
            url_parts_host = url_parts.split(':')
            url_parts = [url_parts]
        else:
            url_parts_host = [url_parts]
            url_parts = [url_parts]
        host = url_parts_host[0]

        #print(type(url_parts))
        # get port
        if (':' in url_parts[-1]):
            url_parts_port = url_parts[-1].split(':')
            url_parts[-1] = url_parts_port[0]
        else:
            url_parts_port = ['80'] # the default port
        port = url_parts_port[-1]

        try:
            port = int(port)
        except:
            raise

        #print(type(url_parts))
        # get path
        if (len(url_parts)>1):
            path = '/'.join(url_parts[1:])
            path = '/' + path
        else:
            path = '/'

        return host, path, port

    def connect(self, host, port):
        # use sockets!
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((host, port))
        return clientSocket

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    # send everything to the socket
    def sendRequest(self, sock, request):
        sock.sendall(request)
        return

    def GET(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )

    print(client.get_host_path_port(sys.argv[2]))
