# Simulation Testbench
#
# Author: Neha Karanjkar
# Date: 6 April 2020

import simpy
from Applications import SendingApplication,ReceivingApplication
from Channel import UnreliableChannel
from Protocol_GBN import rdt_Sender, rdt_Receiver


# Create a simulation environment
env=simpy.Environment()


# Populate the simulation environment with objects:
sending_app	  = SendingApplication(env,sending_interval=1)
receiving_app = ReceivingApplication(env)
rdt_sender	  = rdt_Sender(env=env)
rdt_receiver  = rdt_Receiver(env=env)
# create the DATA and ACK channels and set channel parameters
channel_for_data  = UnreliableChannel(env=env,name="DATA_CHANNEL",Pc=0.1,Pl=0.1,propagation_delay=2, transmission_rate=1000)
channel_for_ack	  = UnreliableChannel(env=env,name="ACK_CHANNEL", Pc=0.1,Pl=0.1,propagation_delay=2, transmission_rate=1000)


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

TOTAL_SIMULATION_TIME=200  # <==== Total simulation time. Increase it as you like.
t=0
while env.peek() <= TOTAL_SIMULATION_TIME:
	if(env.peek()>t):
		rdt_sender.print_status()
	env.step()
	t=int(env.now)
	# We may wish to halt the simulation if some condition occurs.
	# For example, if the receiving application recives 100 messages.
	num_msg = receiving_app.total_messages_received
	if num_msg >= 10: # <=== Halt simulation when receiving application receives these many messages.
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



