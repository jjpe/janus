#! /usr/bin/env python3
# A broker between Monto sources, servers and sinks

# All copyrights reserved (C), 2015, Joey Ezechiels
# This source code in this file is subject to the GPLv3
# as described here: https://gnu.org/licenses/gpl-3.0.txt

import zmq
import gc
import common as c

if __name__ == '__main__':
    gc.disable() # TODO: Use benchmarking to find out if this is useful
    c.broker('product-broker',
             'product',
             c.SocketSpec(zmq.REP, c.FROM_SERVERS, 'from servers'),
             c.SocketSpec(zmq.PUB, c.TO_SINKS,     'to sinks'))

#  LocalWords:  usr txt SocketSpec
