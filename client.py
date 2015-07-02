import sys
from http.client import *

def run():
    address, port = get_arguments()
    connection = HTTPConnection(address, port)
    connection.request('GET', '')
    response = connection.getresponse()
    print(response.read())

def get_arguments():
    arguments = sys.argv
    if len(arguments) != 3:
        error('Usage: python3 client.py <server address> <server port>\nFor example: python3 client.py tahoe.cs.dartmouth.edu 50000')
    address = arguments[1]
    try:
        port = int(arguments[2])
        assert(port >= 1)
    except:
        error("Can't convert {} to a port number ({} should be a positive integer)")
    return address, port

def error(message):
    print(message)
    exit(1)

run()
