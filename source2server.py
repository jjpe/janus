#! /usr/bin/env python3
# A broker between Monto sources, servers and sinks

# All copyrights reserved (C), 2015, Joey Ezechiels
# This source code in this file is subject to the GPLv3
# as described here: https://gnu.org/licenses/gpl-3.0.txt

import montolib
from montolib import FROMSOURCES, TOSERVERS
import zmq
import json
import argparse
import gc

def sourceToServerBroker(tag):
    context = zmq.Context()
    fromsources = context.socket(zmq.REP)
    fromsources.bind(FROMSOURCES)
    print("{} 'from sources' socket bound to {}".format(tag, FROMSOURCES))
    toservers = context.socket(zmq.PUB)
    toservers.bind(TOSERVERS)
    print("{} 'to servers' socket bound to   {}".format(tag, TOSERVERS))
    while True:
        message = fromsources.recv() # msg type is bytes
        fromsources.send(b'ack')
        toservers.send(message)
        decoded_msg = message.decode(encoding='utf-8')
        version = json.loads(decoded_msg)
        montolib.pprint(tag, "Broadcast version:", version)

# def sourceToServerBroker(tag):
#     context = zmq.Context()
#     fromsources = context.socket(zmq.REP)
#     fromsources.bind(FROMSOURCES)
#     print("{} 'from sources' socket bound to {}".format(tag, FROMSOURCES))
#     toservers = context.socket(zmq.PUB)
#     toservers.bind(TOSERVERS)
#     print("{} 'to servers' socket bound to   {}".format(tag, TOSERVERS))
#     poller = zmq.Poller()
#     poller.register(fromsources, zmq.POLLIN)
#     print("{} Registered 'from sources' with poller".format(tag))
#     while True:
#         ready = dict(poller.poll(500))
#         if ready.get(fromsources) == zmq.POLLIN:
#             message = fromsources.recv() # msg type is bytes
#             decoded_msg = message.decode(encoding='utf-8')
#             version = json.loads(decoded_msg)
#             fromsources.send(b'ack')
#             toservers.send(message)
#             montolib.pprint(tag, "Acknowledged, Broadcast version:", version)

if __name__ == "__main__":
    gc.disable() # TODO: Use benchmarking to find out if this is useful
    sourceToServerBroker('[source->server]')
