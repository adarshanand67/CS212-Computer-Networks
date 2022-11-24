# Simulation Testbench
#
# Author: Neha Karanjkar
# Date: 6 April 2020

import simpy
from Applications import SendingApplication, ReceivingApplication
from Channel import UnreliableChannel
from Protocol_SR import rdt_Sender, rdt_Receiver
import numpy as np
import matplotlib.pyplot as plt


'''
======================================
Testbench for Question 1:
======================================
'''

# # Create a simulation environment
# env=simpy.Environment()


# # Populate the simulation environment with objects:
# sending_app	  = SendingApplication(env,sending_interval=1)
# receiving_app = ReceivingApplication(env)
# rdt_sender	  = rdt_Sender(env=env)
# rdt_receiver  = rdt_Receiver(env=env)
# # create the DATA and ACK channels and set channel parameters
# channel_for_data  = UnreliableChannel(env=env,name="DATA_CHANNEL",Pc=0.2,Pl=0.2,propagation_delay=2, transmission_rate=1000)
# channel_for_ack	  = UnreliableChannel(env=env,name="ACK_CHANNEL", Pc=0.2,Pl=0.2,propagation_delay=2, transmission_rate=1000)


# # Set some parameters for the Go-Back-N Protocol
# rdt_sender.N=10	# Window size for the sender
# rdt_receiver.N=10 # Window size for the receiver (Note: This is ignored in the GBN protocol, but required in the SR protocol)
# rdt_sender.K=16 # Packet sequence numbers range from 0 to K-1
# rdt_receiver.K=16 # Packet sequence numbers range from 0 to K-1
# rdt_sender.timeout_value=5	# Timeout value for the sender
# rdt_sender.data_packet_length=1000 # length of the DATA packet in bits
# rdt_receiver.ack_packet_length=10 # length of the ACK packet in bits


# # connect the objects together
# # .....forward path...
# sending_app.rdt_sender = rdt_sender
# rdt_sender.channel = channel_for_data
# channel_for_data.receiver = rdt_receiver
# rdt_receiver.receiving_app = receiving_app
# # ....backward path...for acks
# rdt_receiver.channel = channel_for_ack
# channel_for_ack.receiver = rdt_sender


# # Run simulation, and print status information every now and then.
# # Run the simulation until TOTAL_SIMULATION_TIME elapses OR the receiver receives a certain
# # number of messages in total, whichever occurs earlier.

# TOTAL_SIMULATION_TIME=20000 # <==== Total simulation time. Increase it as you like.
# t=0
# while env.peek() <= TOTAL_SIMULATION_TIME:
# 	if(env.peek()>t):
# 		rdt_sender.print_status()
# 	env.step()
# 	t=int(env.now)
# 	# We may wish to halt the simulation if some condition occurs.
# 	# For example, if the receiving application recives 100 messages.
# 	num_msg = receiving_app.total_messages_received
# 	if num_msg >= 1000: # <=== Halt simulation when receiving application receives these many messages.
# 		print("\n\nReceiving application received",num_msg,"messages. Halting simulation.")
# 		break
# if t==TOTAL_SIMULATION_TIME:
# 	print("\n\nTotal simulation time has elapsed. Halting simulation.")


# # print some statistics at the end of simulation:
# print("===============================================")
# print(" SIMULATION RESULTS:")
# print("===============================================")

# print("Total number of messages sent by the Sending App= %d"%sending_app.total_messages_sent)
# print("Total number of messages received by the Receiving App=%d"%receiving_app.total_messages_received)

# print("Total number of DATA packets sent by rdt_Sender=%d"%rdt_sender.total_packets_sent)
# print("Total number of re-transmitted DATA packets=%d (%0.2f%% of total packets sent)"%(rdt_sender.num_retransmissions,(rdt_sender.num_retransmissions/rdt_sender.total_packets_sent*100.0)))

# print("Total number of ACK packets sent by rdt_Receiver=%d"%rdt_receiver.total_packets_sent)
# print("Total number of re-transmitted ACK packets=%d (%0.2f%% of total packets sent)"%(rdt_receiver.num_retransmissions,(rdt_receiver.num_retransmissions/rdt_receiver.total_packets_sent*100.0)))

# print("Utilization for the DATA channel=%0.2f%%"%(channel_for_data.channel_utilization_time/t*100.0))
# print("Utilization for the  ACK channel=%0.2f%%"%(channel_for_ack.channel_utilization_time/t*100.0))


'''
======================================
Testbench for Question 2:
======================================
'''

# time_taken = []
# channel_utilisation = []
# retransmission_rate = []
# for run in range(5):

# 	# Create a simulation environment
# 	env = simpy.Environment()


# 	# Populate the simulation environment with objects:
# 	sending_app = SendingApplication(env, sending_interval=1)
# 	receiving_app = ReceivingApplication(env)
# 	rdt_sender = rdt_Sender(env=env)
# 	rdt_receiver = rdt_Receiver(env=env)
# 	# create the DATA and ACK channels and set channel parameters
# 	channel_for_data = UnreliableChannel(
# 		env=env, name="DATA_CHANNEL", Pc=0.2, Pl=0.2, propagation_delay=2, transmission_rate=1000)
# 	channel_for_ack = UnreliableChannel(
# 		env=env, name="ACK_CHANNEL", Pc=0.2, Pl=0.2, propagation_delay=2, transmission_rate=1000)


# 	# Set some parameters for the Go-Back-N Protocol
# 	rdt_sender.N = 10  # Window size for the sender
# 	# Window size for the receiver (Note: This is ignored in the GBN protocol, but required in the SR protocol)
# 	rdt_receiver.N = 10
# 	rdt_sender.K = 16  # Packet sequence numbers range from 0 to K-1
# 	rdt_receiver.K = 16  # Packet sequence numbers range from 0 to K-1
# 	rdt_sender.timeout_value = 5  # Timeout value for the sender
# 	rdt_sender.data_packet_length = 1000  # length of the DATA packet in bits
# 	rdt_receiver.ack_packet_length = 10  # length of the ACK packet in bits


# 	# connect the objects together
# 	# .....forward path...
# 	sending_app.rdt_sender = rdt_sender
# 	rdt_sender.channel = channel_for_data
# 	channel_for_data.receiver = rdt_receiver
# 	rdt_receiver.receiving_app = receiving_app
# 	# ....backward path...for acks
# 	rdt_receiver.channel = channel_for_ack
# 	channel_for_ack.receiver = rdt_sender

# 	# <==== Total simulation time. Increase it as you like.
# 	TOTAL_SIMULATION_TIME = 20000
# 	t = 0
# 	while env.peek() <= TOTAL_SIMULATION_TIME:
# 		if(env.peek() > t):
# 			rdt_sender.print_status()
# 		env.step()
# 		t = int(env.now)
# 		# We may wish to halt the simulation if some condition occurs.
# 		# For example, if the receiving application recives 100 messages.
# 		num_msg = receiving_app.total_messages_received
# 		# <=== Halt simulation when receiving application receives these many messages.
# 		if num_msg >= 1000:
# 			print("\n\nReceiving application received",
# 				num_msg, "messages. Halting simulation.")
# 			break
# 	if t == TOTAL_SIMULATION_TIME:
# 		print("\n\nTotal simulation time has elapsed. Halting simulation.")


# 	# print some statistics at the end of simulation:
# 	print("===============================================")
# 	print(" SIMULATION RESULTS:")
# 	print("===============================================")

# 	print("Total number of messages sent by the Sending App= %d" %
# 		sending_app.total_messages_sent)
# 	print("Total number of messages received by the Receiving App=%d" %
# 		receiving_app.total_messages_received)

# 	print("Total number of DATA packets sent by rdt_Sender=%d" %
# 		rdt_sender.total_packets_sent)
# 	print("Total number of re-transmitted DATA packets=%d (%0.2f%% of total packets sent)" %
# 		(rdt_sender.num_retransmissions, (rdt_sender.num_retransmissions/rdt_sender.total_packets_sent*100.0)))

# 	print("Total number of ACK packets sent by rdt_Receiver=%d" %
# 		rdt_receiver.total_packets_sent)
# 	print("Total number of re-transmitted ACK packets=%d (%0.2f%% of total packets sent)" %
# 		(rdt_receiver.num_retransmissions, (rdt_receiver.num_retransmissions/rdt_receiver.total_packets_sent*100.0)))

# 	print("Utilization for the DATA channel=%0.2f%%" %
# 		(channel_for_data.channel_utilization_time/t*100.0))
# 	print("Utilization for the  ACK channel=%0.2f%%" %
# 		(channel_for_ack.channel_utilization_time/t*100.0))

# 	time_taken.append(t)
# 	channel_utilisation.append(channel_for_data.channel_utilization_time/t*100.0)
# 	retransmission_rate.append(rdt_sender.num_retransmissions/rdt_sender.total_packets_sent*100.0)

# print("\n\n")

# # print some statistics at the end of simulation:
# print("===============================================")
# print("5 SIMULATION AVERAGE RESULTS:")
# print("===============================================")

# print("Time taken = ", time_taken)
# print("Channel Utilisation = ", channel_utilisation)
# print("Retransmission Rate = ", retransmission_rate)
# print()
# print("Average time taken for receiving application to receive 1000 msgs: ", sum(time_taken)/len(time_taken))
# print("Average channel utilisation for DATA channel: ", sum(channel_utilisation)/len(channel_utilisation))
# print("Average retransmission rate: ", sum(retransmission_rate)/len(retransmission_rate))

'''
======================================
Testbench for Question 3:
======================================
'''

# time_taken = []
# channel_utilisation = []
# retransmission_rate = []

# for pl in np.arange(0.1, 1.0 , 0.1):
# 	# Create a simulation environment
# 	env = simpy.Environment()

# 	# Populate the simulation environment with objects:
# 	sending_app = SendingApplication(env, sending_interval=1)
# 	receiving_app = ReceivingApplication(env)
# 	rdt_sender = rdt_Sender(env=env)
# 	rdt_receiver = rdt_Receiver(env=env)
# 	# create the DATA and ACK channels and set channel parameters
# 	channel_for_data = UnreliableChannel(
# 		env=env, name="DATA_CHANNEL", Pc=0.2, Pl=pl, propagation_delay=2, transmission_rate=1000)
# 	channel_for_ack = UnreliableChannel(
# 		env=env, name="ACK_CHANNEL", Pc=0.2, Pl=pl, propagation_delay=2, transmission_rate=1000)

# 	# Set some parameters for the Go-Back-N Protocol
# 	rdt_sender.N = 10  # Window size for the sender
# 	# Window size for the receiver (Note: This is ignored in the GBN protocol, but required in the SR protocol)
# 	rdt_receiver.N = 10
# 	rdt_sender.K = 16  # Packet sequence numbers range from 0 to K-1
# 	rdt_receiver.K = 16  # Packet sequence numbers range from 0 to K-1
# 	rdt_sender.timeout_value = 5  # Timeout value for the sender
# 	rdt_sender.data_packet_length = 1000  # length of the DATA packet in bits
# 	rdt_receiver.ack_packet_length = 10  # length of the ACK packet in bits

# 	# connect the objects together
# 	# .....forward path...
# 	sending_app.rdt_sender = rdt_sender
# 	rdt_sender.channel = channel_for_data
# 	channel_for_data.receiver = rdt_receiver
# 	rdt_receiver.receiving_app = receiving_app
# 	# ....backward path...for acks
# 	rdt_receiver.channel = channel_for_ack
# 	channel_for_ack.receiver = rdt_sender

# 	# Run simulation, and print status information every now and then.
# 	# Run the simulation until TOTAL_SIMULATION_TIME elapses OR the receiver receives a certain
# 	# number of messages in total, whichever occurs earlier.

# 	# <==== Total simulation time. Increase it as you like.
# 	TOTAL_SIMULATION_TIME = 20000
# 	t = 0
# 	while env.peek() <= TOTAL_SIMULATION_TIME:
# 		if(env.peek() > t):
# 			rdt_sender.print_status()
# 		env.step()
# 		t = int(env.now)
# 		# We may wish to halt the simulation if some condition occurs.
# 		# For example, if the receiving application recives 100 messages.
# 		num_msg = receiving_app.total_messages_received
# 		# <=== Halt simulation when receiving application receives these many messages.
# 		if num_msg >= 1000:
# 			print("\n\nReceiving application received",
# 				  num_msg, "messages. Halting simulation.")
# 			break
# 	if t == TOTAL_SIMULATION_TIME:
# 		print("\n\nTotal simulation time has elapsed. Halting simulation.")

# 	# # print some statistics at the end of simulation
# 	print("===============================================")
# 	print(" SIMULATION RESULTS:")
# 	print("===============================================")

# 	print("Total number of messages sent by the Sending App= %d" %
# 		  sending_app.total_messages_sent)
# 	print("Total number of messages received by the Receiving App=%d" %
# 		  receiving_app.total_messages_received)

# 	print("Total number of DATA packets sent by rdt_Sender=%d" %
# 		  rdt_sender.total_packets_sent)
# 	print("Total number of re-transmitted DATA packets=%d (%0.2f%% of total packets sent)" %
# 		  (rdt_sender.num_retransmissions, (rdt_sender.num_retransmissions/rdt_sender.total_packets_sent*100.0)))

# 	print("Total number of ACK packets sent by rdt_Receiver=%d" %
# 		  rdt_receiver.total_packets_sent)
# 	print("Total number of re-transmitted ACK packets=%d (%0.2f%% of total packets sent)" %
# 		  (rdt_receiver.num_retransmissions, (rdt_receiver.num_retransmissions/rdt_receiver.total_packets_sent*100.0)))

# 	print("Utilization for the DATA channel=%0.2f%%" %
# 		  (channel_for_data.channel_utilization_time/t*100.0))
# 	print("Utilization for the  ACK channel=%0.2f%%" %
# 		  (channel_for_ack.channel_utilization_time/t*100.0))

# 	time_taken.append(t)
# 	channel_utilisation.append(channel_for_data.channel_utilization_time/t*100.0)
# 	retransmission_rate.append(rdt_sender.num_retransmissions/rdt_sender.total_packets_sent*100.0)

# # plot 3 graphs:
# plt.figure(1)
# plt.plot(np.arange(0.1, 1.0, 0.1), time_taken)
# plt.xlabel("Packet Loss Probability")
# plt.ylabel("Time taken for receiving application to receive 1000 msgs")
# plt.title("Time taken for receiving application to receive 1000 msgs vs Packet Loss Probability")

# plt.figure(2)
# plt.plot(np.arange(0.1, 1.0, 0.1), channel_utilisation)
# plt.xlabel("Packet Loss Probability")
# plt.ylabel("Channel Utilisation")
# plt.title("Channel Utilisation vs Packet Loss Probability")

# plt.figure(3)
# plt.plot(np.arange(0.1, 1.0, 0.1), retransmission_rate)
# plt.xlabel("Packet Loss Probability")
# plt.ylabel("Retransmission Rate")
# plt.title("Retransmission Rate vs Packet Loss Probability")


# plt.show()

'''
======================================
Testbench for Question 6:
======================================
'''

# Create a simulation environment
env=simpy.Environment()


# Populate the simulation environment with objects:
sending_app	  = SendingApplication(env,sending_interval=1)
receiving_app = ReceivingApplication(env)
rdt_sender	  = rdt_Sender(env=env)
rdt_receiver  = rdt_Receiver(env=env)
# create the DATA and ACK channels and set channel parameters
channel_for_data  = UnreliableChannel(env=env,name="DATA_CHANNEL",Pc=0.5,Pl=0.5,propagation_delay=2, transmission_rate=1000)
channel_for_ack	  = UnreliableChannel(env=env,name="ACK_CHANNEL", Pc=0.5,Pl=0.5,propagation_delay=2, transmission_rate=1000)


# Set some parameters for the Go-Back-N Protocol
rdt_sender.N=5	# Window size for the sender
rdt_receiver.N=5 # Window size for the receiver (Note: This is ignored in the GBN protocol, but required in the SR protocol)
rdt_sender.K=32 # Packet sequence numbers range from 0 to K-1
rdt_receiver.K=32 # Packet sequence numbers range from 0 to K-1
rdt_sender.timeout_value=5	# Timeout value for the sender
rdt_sender.data_packet_length=100 # length of the DATA packet in bits
rdt_receiver.ack_packet_length=10 # length of the ACK packet in bits


# connect the objects together
# .....forward path...
sending_app.rdt_sender = rdt_sender
rdt_sender.channel = channel_for_data
channel_for_data.receiver = rdt_receiver
rdt_receiver.receiving_app = receiving_app
# ....backward path...for acks
rdt_receiver.channel = channel_for_ack
channel_for_ack.receiver = rdt_sender


# Run simulation, and print status information every now and then.
# Run the simulation until TOTAL_SIMULATION_TIME elapses OR the receiver receives a certain
# number of messages in total, whichever occurs earlier.

TOTAL_SIMULATION_TIME=20000 # <==== Total simulation time. Increase it as you like.
t=0
while env.peek() <= TOTAL_SIMULATION_TIME:
	if(env.peek()>t):
		rdt_sender.print_status()
	env.step()
	t=int(env.now)
	# We may wish to halt the simulation if some condition occurs.
	# For example, if the receiving application recives 100 messages.
	num_msg = receiving_app.total_messages_received
	if num_msg >= 1000: # <=== Halt simulation when receiving application receives these many messages.
		print("\n\nReceiving application received",num_msg,"messages. Halting simulation.")
		break
if t==TOTAL_SIMULATION_TIME:
	print("\n\nTotal simulation time has elapsed. Halting simulation.")


# print some statistics at the end of simulation:
print("===============================================")
print(" SIMULATION RESULTS:")
print("===============================================")

print("Total number of messages sent by the Sending App= %d"%sending_app.total_messages_sent)
print("Total number of messages received by the Receiving App=%d"%receiving_app.total_messages_received)

print("Total number of DATA packets sent by rdt_Sender=%d"%rdt_sender.total_packets_sent)
print("Total number of re-transmitted DATA packets=%d (%0.2f%% of total packets sent)"%(rdt_sender.num_retransmissions,(rdt_sender.num_retransmissions/rdt_sender.total_packets_sent*100.0)))

print("Total number of ACK packets sent by rdt_Receiver=%d"%rdt_receiver.total_packets_sent)
print("Total number of re-transmitted ACK packets=%d (%0.2f%% of total packets sent)"%(rdt_receiver.num_retransmissions,(rdt_receiver.num_retransmissions/rdt_receiver.total_packets_sent*100.0)))

print("Utilization for the DATA channel=%0.2f%%"%(channel_for_data.channel_utilization_time/t*100.0))
print("Utilization for the  ACK channel=%0.2f%%"%(channel_for_ack.channel_utilization_time/t*100.0))





