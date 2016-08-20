# All copyrights reserved (C), 2015, Joey Ezechiels
# This source code in this file is subject to the GPLv3
# as described here: https://gnu.org/licenses/gpl-3.0.txt

import zmq
import json
import argparse
import gc
from collections import namedtuple

# Default addresses
FROM_SOURCES = b'tcp://127.0.0.1:5000'
TO_SERVERS =   b'tcp://127.0.0.1:5001'
FROM_SERVERS = b'tcp://127.0.0.1:5002'
TO_SINKS =     b'tcp://127.0.0.1:5003'

SocketSpec = namedtuple('SocketSpec', ['type', 'address', 'name'])

def pprint(tag, log_msg, message):
    json_string = json.dumps(message, sort_keys=True, indent=4)
    print("{} {} {}".format(tag, log_msg, json_string))

def log(tag, socketName, address):
    print("{} '{}' socket bound to {}".format(tag, socketName, address))

def broker(tag, messageType, fromSocketSpec, toSocketSpec):
    ''' Define a new broker.
tag:             A tag to prepend to each log message
messageType:     Either the string 'version' or 'product'
fromSocketSpec:  A SocketSpec named tuple that describes the incoming socket
toSocketSpec:    A SocketSpec named tuple that describes the outgoing socket'''
    context = zmq.Context()
    fromSocket = context.socket(fromSocketSpec.type)
    fromSocket.bind(fromSocketSpec.address)
    log(tag, fromSocketSpec.name, fromSocketSpec.address)
    toSocket = context.socket(toSocketSpec.type)
    toSocket.bind(toSocketSpec.address)
    log(tag, toSocketSpec.name, toSocketSpec.address)
    while True:
        message = fromSocket.recv() # msg type is bytes
        fromSocket.send(b'ack')
        toSocket.send(message)
        version = json.loads(message.decode('utf-8'))
