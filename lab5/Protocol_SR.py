# SimPy models for rdt_Sender and rdt_Receiver
# implementing the Selective Repeat Protocol

# Author: Aniket Chaudhri, IIT Goa

import simpy
import random
import sys
from Packet import Packet

class rdt_Sender(object):
	
	def __init__(self, env):
		# Initialize variables and parameters
		self.env = env
		self.channel = None

		# some default parameter values
		self.data_packet_length = 10  # bits
		self.timeout_value = 10  # default timeout value for the sender
		self.N = 5  # Sender's Window size
		self.K = 16  # Packet Sequence numbers can range from 0 to K-1

		# some state variables and parameters for the Go-Back-N Protocol
		self.base = 1  # base of the current window
		self.nextseqnum = 1  # next sequence number
		# a buffer for storing the packets to be sent (implemented as a Python dictionary)
		self.sndpkt = {}

		# some other variables to maintain sender-side statistics
		self.total_packets_sent = 0
		self.num_retransmissions = 0

		# timer for each packet
		self.timer = {}
		self.timer_is_running = {}

		# store which packets have been acked
		self.acked = {}
		# self.acked = []

		# buffer to store the packets received from the upper layer 
		self.buffer = []



		
	def rdt_send(self,msg):
		# This function is called by the upper-layer 
		# when a packet arrives at the sender
		if (self.nextseqnum in [(self.base+i)%self.K for i in range(0,self.N)]):
			# create a new packet and store a copy of it in the buffer
			packt_to_send = Packet(seq_num=self.nextseqnum, payload=msg, packet_length=self.data_packet_length)
			self.sndpkt[self.nextseqnum]=packt_to_send
			# send the packet
			self.channel.udt_send(packt_to_send)
			self.total_packets_sent+=1
			# start the timer
			# self.timer[self.nextseqnum]=self.env.timeout(self.timeout_value)
			self.start_timer(self.nextseqnum)
			# update nextseqnum
			self.nextseqnum=(self.nextseqnum+1)%self.K
			return True
		else:
			# self.buffer.append(Packet(seq_num=self.nextseqnum, payload=msg, packet_length=self.data_packet_length))
			# # update nextseqnum
			# self.nextseqnum = (self.nextseqnum+1) % self.K			
			return False
			# return True

	def rdt_rcv(self,packt):
		if (packt.corrupted==False):
			# mark the packet as acked
			if (packt.seq_num in self.sndpkt.keys()):
				self.acked[packt.seq_num]=True
				# self.acked.append(packt.seq_num)
				# check if the acked packet is the base
				if (packt.seq_num==self.base):
					# find the next base
					while(self.base in self.acked.keys()):
						# self.acked.remove(self.base)
						del self.acked[self.base]
						del self.sndpkt[self.base]
						self.stop_timer(self.base)
						# delete from the buffer
						
						self.base = (self.base+1) % self.K
					
				# else:
				# 	# stop the timer for recived packet
				# 	self.stop_timer(packt.seq_num)
	
	def timer_behavior(self, seq_num):
		try:
			# Wait for timeout 
			self.timer_is_running[seq_num]=True
			yield self.env.timeout(self.timeout_value)
			self.timer_is_running[seq_num]=False
			# take some actions 
			self.timeout_action(seq_num)
		except simpy.Interrupt:
			# stop the timer
			self.timer_is_running[seq_num]=False

	
	def start_timer(self, seq_num):
		# self.timer = self.env.process(self.timer_behavior())
		# print("TIME:", self.env.now, "TIMER STARTED for a timeout of ", self.timeout_value)
		# print("start timer called", seq_num)
		self.timer[seq_num] = self.env.process(self.timer_behavior(seq_num))
		# print(self.timer[seq_num])
		print("TIME:", self.env.now, "TIMER STARTED for a timeout of ", self.timeout_value, "for packet", seq_num)

	def stop_timer(self, seq_num):
		# print("TIME:", self.env.now, "TIMER STOPPED")
		# print("stop timer called", seq_num)
		assert(self.timer_is_running[seq_num]==True)
		# print(self.timer[seq_num])
		self.timer[seq_num].interrupt()
		print("TIME:", self.env.now, "TIMER STOPPED for packet", seq_num)

		

	# # Actions to be performed upon timeout
	def timeout_action(self, seq_num):

		self.channel.udt_send(self.sndpkt[seq_num])
		self.num_retransmissions += 1
		self.total_packets_sent += 1
		self.start_timer(seq_num)

	# A function to print the current window position for the sender.
	def print_status(self):
		print("TIME:",self.env.now,"Current window:", [(self.base+i)%self.K for i in range(0,self.N)],"base =",self.base,"nextseqnum =",self.nextseqnum)
		print("---------------------")





class rdt_Receiver(object):
	
	def __init__(self,env):
		
		# Initialize variables
		self.env=env 
		self.receiving_app=None
		self.channel=None

		# some default parameter values
		self.ack_packet_length=10 # bits
		self.K = 5 # range of sequence numbers expected
		self.N = 16  # Receiver's Window size

		#initialize state variables
		# self.expectedseqnum=1
		# self.sndpkt= Packet(seq_num=0, payload="ACK",packet_length=self.ack_packet_length)
		self.total_packets_sent=0
		self.num_retransmissions=0

		# some state variables and parameters for the Go-Back-N Protocol
		self.base=1 # base of the current window 
		# self.nextseqnum=1 # next sequence number
		self.buffer= {} # a buffer for storing the packets to be sent (implemented as a Python dictionary)

		

	def rdt_rcv(self,packt):
		# This function is called by the lower-layer 
		# when a packet arrives at the receiver
		if (packt.corrupted==False):
			if (packt.seq_num in [(self.base+i)%self.K for i in range(0,self.N)]):
				print("TIME:",self.env.now,"RDT_RECEIVER: rdt_rcv() called for seq_num=",packt.seq_num," within current window. Sending ACK.")
				# create a new packet and store a copy of it in the buffer
				packt_to_send = Packet(seq_num=packt.seq_num, payload="ACK", packet_length=self.ack_packet_length)
				# send the packet
				self.channel.udt_send(packt_to_send)
				self.total_packets_sent+=1
				# self.base = (packt.seq_num+1)%self.K
				# if packet not received earlier, buffer it
				# if packt.seq_num not in self.buffer:
				self.buffer[packt.seq_num]=packt

				# print currently buffered packets with their payload and sequence numbers
				print("\nTIME:",self.env.now,"RDT_RECEIVER: Currently buffered packets:")
				for key in self.buffer:
					print("TIME:",self.env.now,"RDT_RECEIVER: Packet with seq_num=",key," and payload=",self.buffer[key].payload)
				print('\n')
				# print("TIME:",self.env.now,"RDT_RECEIVER: Currently buffered packets:",self.buffer.keys())
				
				if packt.seq_num == self.base:
					print('base', self.base)
					# deliver all the buffered packets
					while self.base in self.buffer.keys():
						# deliver the packet
						self.receiving_app.deliver_data(self.buffer[self.base].payload)
						# delete the packet from the buffer
						del self.buffer[self.base]
						# update the base
						self.base = (self.base+1)%self.K

			elif (packt.seq_num in [(self.base-self.N + i)%self.K for i in range(0,self.N)]):
				print("TIME:",self.env.now,"RDT_RECEIVER: rdt_rcv() called for seq_num=",packt.seq_num," already delivered to app. Still Sending ACK.")
				# create a new packet and store a copy of it in the buffer
				packt_to_send = Packet(seq_num=packt.seq_num, payload="ACK", packet_length=self.ack_packet_length)
				# send the packet
				self.channel.udt_send(packt_to_send)
				self.total_packets_sent+=1

			
