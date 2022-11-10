# SimPy model for the Reliable Data Transport (rdt) Protocol 2.0 (Using ACK and NAK)

#
# Sender-side (rdt_Sender)
#	- receives messages to be delivered from the upper layer 
#	  (SendingApplication) 
#	- Implements the protocol for reliable transport
#	 using the udt_send() function provided by an unreliable channel.
#
# Receiver-side (rdt_Receiver)
#	- receives packets from the unrealible channel via calls to its
#	rdt_rcv() function.
#	- implements the receiver-side protocol and delivers the collected
#	data to the receiving application.

# Author: Neha Karanjkar
# Modified by: Rajat Singh (2003130)
#              Raj Hans Khoiwal (2003129)


from os import stat
import simpy
import random
from Packet import Packet
import sys

# the sender can be in one of these two states:
SENDER_WAITING_FOR_CALL_ZERO_FROM_ABOVE = 0
SENDER_WAITING_FOR_CALL_ONE_FROM_ABOVE = 1
WAIT_FOR_ACK_ZERO = 2
WAIT_FOR_ACK_ONE = 3
RECIEVER_WAITING_FROM_CALL_ZERO_FROM_ABOVE = 4
RECIEVER_WAITING_FROM_CALL_ONE_FROM_ABOVE = 5


class rdt_Sender(object):
    def __init__(self,env):
        # Initialize variables
        self.env=env 
        self.channel=None
		# some state variables
        self.state = SENDER_WAITING_FOR_CALL_ZERO_FROM_ABOVE
        self.packet_to_be_sent=None

    def rdt_send(self,msg):
        if self.state==SENDER_WAITING_FOR_CALL_ZERO_FROM_ABOVE:
			# This function is called by the 
			# sending application.
			# create a packet, and save a copy of this packet
			# for retransmission, if needed
            self.packet_to_be_sent = Packet(seq_num=0, payload=msg)
			# send it over the channel
            self.channel.udt_send(self.packet_to_be_sent)
            # wait for an ACK or NAK
            self.state=WAIT_FOR_ACK_ZERO
            return True
        
        elif self.state==SENDER_WAITING_FOR_CALL_ONE_FROM_ABOVE:
            # This function is called by the 
			# sending application.
			# create a packet, and save a copy of this packet
			# for retransmission, if needed
            self.packet_to_be_sent = Packet(seq_num=1, payload=msg)
			# send it over the channel
            self.channel.udt_send(self.packet_to_be_sent)
            # wait for an ACK or NAK
            self.state=WAIT_FOR_ACK_ONE
            return True
        
        else:
            return False
            
        
    def rdt_rcv(self,packt):
		# This function is called by the lower-layer 
		# # when an ACK=0/ACK=1 packet arrives
        # assert(self.state==WAIT_FOR_ACK_ZERO or self.state==WAIT_FOR_ACK_ONE)

        if (self.state==WAIT_FOR_ACK_ZERO):
            if (packt.corrupted or (packt.payload=="ACK" and packt.seq_num==1)):
			    # Received a ACK,1 or pkt is corrupted. Need to resend packet.
                self.channel.udt_send(self.packet_to_be_sent)
            elif (not packt.corrupted and (packt.payload=="ACK" and packt.seq_num==0)):
			    # Received an ACK,0. Everything's fine.
                self.state=SENDER_WAITING_FOR_CALL_ONE_FROM_ABOVE

        elif (self.state==WAIT_FOR_ACK_ONE):
            if (packt.corrupted or (packt.payload=="ACK" and packt.seq_num==0)):
			    # Received a ACK,0 or pkt is corrupted. Need to resend packet.
                self.channel.udt_send(self.packet_to_be_sent)
            elif (not packt.corrupted and (packt.payload=="ACK" and packt.seq_num==1)):
			    # Received an ACK,1. Everything's fine.
                self.state=SENDER_WAITING_FOR_CALL_ZERO_FROM_ABOVE

			

class rdt_Receiver(object):
    def __init__(self,env):
        # Initialize variables
        self.env=env
        self.state=RECIEVER_WAITING_FROM_CALL_ZERO_FROM_ABOVE
        self.receiving_app=None
        self.channel=None
        self.packet_to_be_sent=None
		
    def rdt_rcv(self,packt):
		# This function is called by the lower-layer when a packet arrives
		# at the receiver
		
        if(self.state==RECIEVER_WAITING_FROM_CALL_ZERO_FROM_ABOVE):
            if(packt.corrupted or packt.seq_num==1):
                # Recieved a seq=1 or pkt is corrupted. Need to resend packet.
                self.packet_to_be_sent = Packet(seq_num=1, payload="ACK")
                self.channel.udt_send(self.packet_to_be_sent)
            
            elif(not packt.corrupted and packt.seq_num==0):
                # send it over the channel
                self.receiving_app.deliver_data(packt.payload)
                # The packet is not corrupted.
                # Send an ACK,0 and deliver the data.
                self.packet_to_be_sent = Packet(seq_num=0, payload="ACK") 
                self.channel.udt_send(self.packet_to_be_sent)
                self.state=RECIEVER_WAITING_FROM_CALL_ONE_FROM_ABOVE

        elif(self.state==RECIEVER_WAITING_FROM_CALL_ONE_FROM_ABOVE):
            if(packt.corrupted or packt.seq_num==0):
                # Recieved a seq=0 or pkt is corrupted. Need to resend packet.
                self.packet_to_be_sent = Packet(seq_num=0, payload="ACK")
                self.channel.udt_send(self.packet_to_be_sent)
            
            elif(not packt.corrupted and packt.seq_num==1):
                # send it over the channel
                self.receiving_app.deliver_data(packt.payload)
                # The packet is not corrupted.
                # Send an ACK,1 and deliver the data.
                self.packet_to_be_sent = Packet(seq_num=1, payload="ACK") 
                self.channel.udt_send(self.packet_to_be_sent)
                self.state=RECIEVER_WAITING_FROM_CALL_ZERO_FROM_ABOVE



