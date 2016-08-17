# -*- coding: utf-8 -*-
"""
Created on Sun Aug 07 00:03:34 2016

@author: Badger
"""

import open_bci_v3 as bci
import json
from Queue import Queue
from twisted.internet.defer import inlineCallbacks, CancelledError 
import sys
import os
import time

from twisted.python import log
from twisted.internet import reactor, threads
from autobahn.twisted.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
    
    
queue = Queue()

order_number = 0
last_packet_id = None


def read_samples():
     # USB dongle settings    
    port = "COM3"
    baud = 115200
    # connect to board
    board = bci.OpenBCIBoard(port=port, baud=baud, filter_data=False)
    board.start_streaming(process_sample)

    
def process_sample(sample):
    """ format sample as json string and add it to queue """
    global last_packet_id
    global order_number 
    if last_packet_id is not None:
        # it is assumed that no more than 255 packets are skipped
        difference = (sample.id - last_packet_id) % 256
        order_number = order_number + difference
    last_packet_id = sample.id
    dict_sample = {
        "channel_data": sample.channel_data,
        "order_number": order_number
    }
    json_sample = json.dumps(dict_sample)
    queue.put(json_sample)
    

def wait_for_sample():
    """ defer queue reading """
    d = threads.deferToThread(read_queue)
    #reactor.callLater(0, read_queue, d.callback)
    timeout = reactor.callLater(5, d.cancel)
    def cancel_timeout(result):
        if timeout.active():
            timeout.cancel()
        return result
    d.addBoth(cancel_timeout)
    return d
    

def read_queue():
    ### get sample values stored in queue and give results to Deferred ###
    sample = queue.get()
    return sample
    

class MyClientProtocol(WebSocketClientProtocol):

    def onConnect(self, response):
        print("Server connected: {0}".format(response.peer))
        
    @inlineCallbacks     
    def onOpen(self):
        print("WebSocket connection open.")
        while True:
            try:                
                sample = yield wait_for_sample()
                self.sendMessage(sample)
            except CancelledError:
                self.sendClose()

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        os._exit(0)
        
if __name__ == '__main__':

    log.startLogging(sys.stdout)

    factory = WebSocketClientFactory("ws://tassi.fi:1912/api/samples")
    factory.protocol = MyClientProtocol

    reactor.connectTCP("tassi.fi", 1912, factory)
    reactor.callInThread(read_samples)
    reactor.run()

"""
import socket
import open_bci_v3 as bci
import json

sock = None


# configure board and server connection
def start_streaming():
    # USB dongle settings    
    port = "COM3"
    baud = 115200
    # server target
    tcp_ip = "127.0.0.1"    
    tcp_port = 1912
    # open connection to server
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((tcp_ip, tcp_port))
    # connect to board
    board = bci.OpenBCIBoard(port=port, baud=baud, filter_data=False)
    board.start_streaming(process_sample)


# format sample as json string
def process_sample(sample):
    dict_sample = {
        "id": sample.id,
        "channel_data": sample.channel_data
    }
    
    json_sample = json.dumps(dict_sample)
    send_sample(json_sample)

    
# send sample data to server    
def send_sample(json_sample):
   
    sock.send(json_sample)
    
    
if __name__ == "__main__":
    start_streaming()
    
"""