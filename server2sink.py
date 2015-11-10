#! /usr/bin/env python3
# A broker between Monto sources, servers and sinks

# All copyrights reserved (C), 2015, Joey Ezechiels
# This source code in this file is subject to the GPLv3
# as described here: https://gnu.org/licenses/gpl-3.0.txt

import montolib
from montolib import FROMSERVERS, TOSINKS
import zmq
import json
import argparse
import gc

def serverToSinkBroker(tag):
    context = zmq.Context()
    fromservers = context.socket(zmq.REP)
    fromservers.bind(montolib.FROMSERVERS)
    print("{} 'from servers' socket bound to {}".format(tag, FROMSERVERS))
    tosinks = context.socket(zmq.PUB)
    tosinks.bind(TOSINKS)
    print("{} 'to sinks' socket bound to     {}".format(tag, TOSINKS))
    while True:
        message = fromservers.recv()
        fromservers.send(b'ack')
        tosinks.send(message)
        decoded_msg = message.decode('utf-8')
        product = json.loads(decoded_msg)
        montolib.pprint(tag, "Broadcast product:", product)

# def serverToSinkBroker(tag):
#     context = zmq.Context()
#     fromservers = context.socket(zmq.REP)
#     fromservers.bind(montolib.FROMSERVERS)
#     print("{} 'from servers' socket bound to {}".format(tag, FROMSERVERS))
#     tosinks = context.socket(zmq.PUB)
#     tosinks.bind(TOSINKS)
#     print("{} 'to sinks' socket bound to     {}".format(tag, TOSINKS))
#     poller = zmq.Poller()
#     poller.register(fromservers, zmq.POLLIN)
#     print("{} Registered 'from servers' with poller".format(tag))
#     while True:
#         ready = dict(poller.poll(500))
#         if ready.get(fromservers) == zmq.POLLIN:
#             message = fromservers.recv()
#             decoded_msg = message.decode('utf-8')
#             product = json.loads(decoded_msg)
#             fromservers.send(b'ack')
#             tosinks.send(message)
#             montolib.pprint(tag, "Acknowledged, Broadcast product:", product)

if __name__ == '__main__':
    gc.disable() # TODO: Use benchmarking to find out if this is useful
    serverToSinkBroker('[server->sink]')
