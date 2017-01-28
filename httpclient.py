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

    # def __str__(self):
    #     return str(self.code) + ' ' + str(self.body)

class HTTPClient(object):
    def get_host_path_port(self,url):
        if not len(url)>0:
            raise

        # get rid of protocal
        if ('://' in url):
            url_parts = url.split('://')
            url_parts = url_parts[1]
        else:
            url_parts = url

        # get format [host (or host:port), path, path, ... ]
        if ('/' in url_parts):
            url_parts = url_parts.split('/')
        else:
            url_parts = [url_parts]

        # get host and port
        if (':' in url_parts[0]):
            url_parts_host_port = url_parts[0].split(':')
        else:
            url_parts_host_port = [url_parts[0],'80']
        host = url_parts_host_port[0]
        port = url_parts_host_port[1]

        try:
            port = int(port)
        except:
            raise

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
        data_parts = data.split('\r\n')
        code = data_parts[0].split()[1]
        return int(code)

    def get_headers(self,data):
        data_parts = data.split('\r\n\r\n')
        headers = data_parts[0].split('\r\n')[1:]
        return headers

    def get_body(self, data):
        data_parts = data.split('\r\n\r\n')
        if(len(data_parts)>1):
            body = data_parts[1]
        else:
            body = ""
        return body

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

    def GET(self, url, args=None):
        # print(url)
        if not (len(url)>0):
            return HTTPResponse(404,"")

        # set up connection
        host, path, port = self.get_host_path_port(url)
        connection = self.connect(host,port)

        # send request
        # request = "GET / HTTP/1.0\r\n\r\n"
        request = 'GET ' + path + ' HTTP/1.1\r\n' + \
                  'Host: ' + host + '\r\n' + \
                  'User-Agent: httpclient.py\r\n' + \
                  'Accept: */*\r\n' + \
                  '\r\n'

        connection.sendall(request)

        # got response
        response = self.recvall(connection)

        # decoding
        code = self.get_code(response)
        body = self.get_body(response)

        # disconnect
        connection.close()

        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        # print(url)
        if not (len(url)>0):
            return HTTPResponse(404,"")

        # set up connection
        host, path, port = self.get_host_path_port(url)
        connection = self.connect(host,port)

        # get arguments ready
        contents = ""
        if (args!=None):
            contents = urllib.urlencode(args)
        # print(type(args))

        # send request
        request = 'POST ' + path + ' HTTP/1.1\r\n' + \
                  'Host: ' + host + '\r\n' + \
                  'User-Agent: httpclient.py\r\n' + \
                  'Content-Length: ' + str(len(contents)) + '\r\n' + \
                  'Content-Type: application/x-www-form-urlencoded\r\n' + \
                  'Accept: */*\r\n' + \
                  '\r\n' + \
                  contents

        connection.sendall(request)

        # got response
        response = self.recvall(connection)

        # decoding
        code = self.get_code(response)
        body = self.get_body(response)

        # disconnect
        connection.close()

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

    # print(client.get_host_path_port(sys.argv[2]))
