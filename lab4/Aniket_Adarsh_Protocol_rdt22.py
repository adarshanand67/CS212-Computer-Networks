# SimPy model for the Reliable Data Transport (rdt) Protocol 2.2 (Using ACK and NAK)
'''
Team Members:
    1. Aniket Akshay Chaudhri (2003104)
    2. Adarsh Anand (2003101)
'''

import simpy
import random
from Packet import Packet
import sys

# the sender can be in one of these four states:
WAITING_FOR_CALL_0_FROM_ABOVE = 0
WAIT_FOR_ACK_0 = 1
WAITING_FOR_CALL_1_FROM_ABOVE = 2
WAIT_FOR_ACK_1 = 3


class rdt_Sender(object):
    def __init__(self, env):
        # Initialize variables
        self.env = env
        self.channel = None

        # some state variables
        self.state = WAITING_FOR_CALL_0_FROM_ABOVE
        self.seq_num = 0
        self.packet_to_be_sent = None

        # keep track of start and end times
        self.start_time = env.now
        self.end_time = None
        self.rtt = []

    def rdt_send(self, msg):

        if self.state == WAITING_FOR_CALL_0_FROM_ABOVE:
            # This function is called by the
            # sending application.

            # create a packet, and save a copy of this packet
            # for retransmission, if needed
            self.seq_num = 0
            self.packet_to_be_sent = Packet(seq_num=self.seq_num, payload=msg)
            
            # start time
            self.start_time = self.env.now

            # send it over the channel
            self.channel.udt_send(self.packet_to_be_sent)
            # wait for an ACK or NAK
            self.state = WAIT_FOR_ACK_0
            return True
        elif self.state == WAITING_FOR_CALL_1_FROM_ABOVE:
            # This function is called by the
            # sending application.

            # create a packet, and save a copy of this packet
            # for retransmission, if needed
            self.seq_num = 1
            self.packet_to_be_sent = Packet(seq_num=self.seq_num, payload=msg)
            
            # start time
            self.start_time = self.env.now

            # send it over the channel
            self.channel.udt_send(self.packet_to_be_sent)
            # wait for an ACK or NAK
            self.state = WAIT_FOR_ACK_1
            return True
        else:
            return False

    def rdt_rcv(self, packt):
        # This function is called by the lower-layer
        # when an ACK/NAK packet arrives
       
        if self.state == WAIT_FOR_ACK_0:
            if packt.payload == "ACK" and packt.seq_num == 0:
                # packet is fine
                self.end_time = self.env.now
                self.rtt.append(self.end_time - self.start_time)
                self.state = WAITING_FOR_CALL_1_FROM_ABOVE
            else:
                self.channel.udt_send(self.packet_to_be_sent) # retransmit
        elif self.state == WAIT_FOR_ACK_1:
            if packt.payload == "ACK" and packt.seq_num == 1:
                # packet is fine
                self.end_time = self.env.now
                self.rtt.append(self.end_time - self.start_time)
                self.state = WAITING_FOR_CALL_0_FROM_ABOVE
            else:
                self.channel.udt_send(self.packet_to_be_sent) # retransmit


class rdt_Receiver(object):
    def __init__(self, env):
        # Initialize variables
        self.env = env
        self.channel = None
        self.receiving_app = None

        # some state variables
        self.state = WAITING_FOR_CALL_0_FROM_ABOVE
        self.seq_num = 0
        self.packet_to_be_sent = None

    def rdt_rcv(self, packt):
        # This function is called by the lower-layer
        # when a packet arrives
        if self.state == WAITING_FOR_CALL_0_FROM_ABOVE:
            if packt.corrupted or packt.seq_num == 1: # packet is corrupted or not the one expected
                self.channel.udt_send(Packet(seq_num=1, payload="ACK"))
            else: # packet is fine
                self.receiving_app.deliver_data(packt.payload)
                self.channel.udt_send(Packet(seq_num=0, payload="ACK"))
                self.state = WAITING_FOR_CALL_1_FROM_ABOVE
        
        elif self.state == WAITING_FOR_CALL_1_FROM_ABOVE:
            if packt.corrupted or packt.seq_num == 0: # packet is corrupted or not the one expected
                self.channel.udt_send(Packet(seq_num=0, payload="ACK"))
            else: # packet is fine
                self.receiving_app.deliver_data(packt.payload)
                self.channel.udt_send(Packet(seq_num=1, payload="ACK"))
                self.state = WAITING_FOR_CALL_0_FROM_ABOVE
