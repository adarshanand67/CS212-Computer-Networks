# Simpy implememtation of the protocol rdt3.0
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
        
        self.env= env
        self.channel = None

        # additional timer-related variables
        self.timer = None
        self.timeout_value=6
        self.timer_is_running=False

        # some state variables
        self.state = WAITING_FOR_CALL_0_FROM_ABOVE
        self.seq_num = 0
        self.packet_to_be_sent = None

        # keep track of start and end times
        self.start_time = env.now
        self.end_time = None
        self.rtt = []

        self.total_acks_recv = 0

    # This function models a Timer's behavior.
    def timer_behavior(self):
        try:
        # Start
            self.timer_is_running=True
            yield self.env.timeout(self.timeout_value)
            # Stop
            self.timer_is_running=False
            # take some actions
            self.timeout_action()
        except simpy.Interrupt:
            # upon interrupt, stop the timer
            self.timer_is_running=False
            
    # This function can be called to start the timer.
    def start_timer(self):
        assert(self.timer_is_running==False)
        self.timer=self.env.process(self.timer_behavior())
        
    # This function can be called to stop the timer
    def stop_timer(self):
        assert(self.timer_is_running==True)
        self.timer.interrupt()

    def timeout_action(self):
        self.channel.udt_send(self.packet_to_be_sent)
        self.start_timer()


    def rdt_send(self, msg):
        if self.state == WAITING_FOR_CALL_0_FROM_ABOVE:
            # This function is called by the sending application.
            # create a packet, and save a copy of this packet
            # for retransmission, if needed
            self.packet_to_be_sent = Packet(seq_num=0, payload=msg)
            # send it over the channel
            self.start_time = self.env.now
            self.channel.udt_send(self.packet_to_be_sent)
            # wait for an ACK or NAK
            self.start_timer()
            self.state = WAIT_FOR_ACK_0
            return True

        elif self.state == WAITING_FOR_CALL_1_FROM_ABOVE:
            # This function is called by the sending application.
            # create a packet, and save a copy of this packet
            # for retransmission, if needed
            self.packet_to_be_sent = Packet(seq_num=1, payload=msg)
            # send it over the channel
            self.start_time = self.env.now
            self.channel.udt_send(self.packet_to_be_sent)
            # wait for an ACK or NAK
            self.start_timer()
            self.state = WAIT_FOR_ACK_1
            return True

    def rdt_rcv(self, packt):
        if self.state == WAIT_FOR_ACK_0:
            if (not packt.corrupted and (packt.payload=="ACK" and packt.seq_num==0) and self.timer_is_running):
                self.stop_timer()
                self.state = WAITING_FOR_CALL_1_FROM_ABOVE
                self.seq_num = 1
                self.end_time = self.env.now
                self.rtt.append(self.end_time - self.start_time)
                self.total_acks_recv += 1
                return True
        elif self.state == WAIT_FOR_ACK_1:
            if (not packt.corrupted and (packt.payload=="ACK" and packt.seq_num==1) and self.timer_is_running):
                self.stop_timer()
                self.state = WAITING_FOR_CALL_0_FROM_ABOVE
                self.seq_num = 0
                self.end_time = self.env.now
                self.rtt.append(self.end_time - self.start_time)
                self.total_acks_recv += 1
                return True


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
            if packt.corrupted or packt.seq_num == 1: # if corrupted or seq_num is 1
                self.channel.udt_send(Packet(seq_num=1, payload="ACK"))
            else: # packet is fine
                self.receiving_app.deliver_data(packt.payload)
                self.channel.udt_send(Packet(seq_num=0, payload="ACK"))
                self.state = WAITING_FOR_CALL_1_FROM_ABOVE

        elif self.state == WAITING_FOR_CALL_1_FROM_ABOVE:
            if packt.corrupted or packt.seq_num == 0: # if corrupted or seq_num is 0
                self.channel.udt_send(Packet(seq_num=0, payload="ACK"))
            else: # packet is fine
                self.receiving_app.deliver_data(packt.payload)
                self.channel.udt_send(Packet(seq_num=1, payload="ACK"))
                self.state = WAITING_FOR_CALL_0_FROM_ABOVE
