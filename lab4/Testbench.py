# Simulation Testbench
#
# Author: Neha Karanjkar


import matplotlib.pyplot as plt
import simpy
import numpy as np
from Applications import SendingApplication,ReceivingApplication
from Channel import UnreliableChannel
from lab4.Aniket_Adarsh_Protocol_rdt3 import *

# Create a simulation environment
env=simpy.Environment()


# Populate the simulation environment with objects:
sending_app	  = SendingApplication(env)
receiving_app = ReceivingApplication(env)
rdt_sender	  = rdt_Sender(env)
rdt_receiver  = rdt_Receiver(env)
channel_for_data  = UnreliableChannel(env=env,Pc=0.5,Pl=0.1,delay=2,name="DATA_CHANNEL")
channel_for_ack	  = UnreliableChannel(env=env,Pc=0.5,Pl=0.1,delay=2,name="ACK_CHANNEL")

# connect the objects together
# .....forward path...
sending_app.rdt_sender = rdt_sender
rdt_sender.channel = channel_for_data
channel_for_data.receiver = rdt_receiver
rdt_receiver.receiving_app = receiving_app
# ....backward path...for acks
rdt_receiver.channel = channel_for_ack
channel_for_ack.receiver = rdt_sender

# Run simulation
env.run(until=receiving_app.isCompleted)
print("T_avg:", sum(rdt_sender.rtt)/len(rdt_sender.rtt))

# env.run(until=100)
# env.run()

# t_avgs = []
# # run for pc from 0 to 0.9
# for pc in np.arange(0,0.9,0.1):
#     # Create a simulation environment
#     env=simpy.Environment()

#     # Populate the simulation environment with objects:
#     sending_app	  = SendingApplication(env)
#     receiving_app = ReceivingApplication(env)
#     rdt_sender	  = rdt_Sender(env)
#     rdt_receiver  = rdt_Receiver(env)
#     channel_for_data  = UnreliableChannel(env=env,Pc=pc,Pl=0,delay=2,name="DATA_CHANNEL")
#     channel_for_ack	  = UnreliableChannel(env=env,Pc=0,Pl=0,delay=2,name="ACK_CHANNEL")

#     # connect the objects together
#     # .....forward path...
#     sending_app.rdt_sender = rdt_sender
#     rdt_sender.channel = channel_for_data
#     channel_for_data.receiver = rdt_receiver
#     rdt_receiver.receiving_app = receiving_app
#     # ....backward path...for acks
#     rdt_receiver.channel = channel_for_ack
#     channel_for_ack.receiver = rdt_sender

#     # Run simulation
#     env.run(until=receiving_app.isCompleted)
#     current_t_avg = float('inf')
#     if len(rdt_sender.rtt) > 0:
#         current_t_avg = sum(rdt_sender.rtt)/len(rdt_sender.rtt)
#     t_avgs.append(current_t_avg)
#     print("T_avg:", current_t_avg)

# # plot the results
# import matplotlib.pyplot as plt
# plt.plot(t_avgs)
# plt.xlabel("Pc")
# plt.ylabel("T_avg")

# # beautify plot
# # plt.xticks(np.arange(0,0.9,0.1))


# plt.show()

# t_avgs = []
# # run for pc from 0 to 0.9
# for pl in np.arange(0, 0.9, 0.01):
#     # Create a simulation environment
#     env = simpy.Environment()

#     # Populate the simulation environment with objects:
#     sending_app = SendingApplication(env)
#     receiving_app = ReceivingApplication(env)
#     rdt_sender = rdt_Sender(env)
#     rdt_receiver = rdt_Receiver(env)
#     channel_for_data = UnreliableChannel(
#         env=env, Pc=0.2, Pl=pl, delay=2, name="DATA_CHANNEL")
#     channel_for_ack = UnreliableChannel(
#         env=env, Pc=0.2, Pl=pl, delay=2, name="ACK_CHANNEL")

#     # connect the objects together
#     # .....forward path...
#     sending_app.rdt_sender = rdt_sender
#     rdt_sender.channel = channel_for_data
#     channel_for_data.receiver = rdt_receiver
#     rdt_receiver.receiving_app = receiving_app
#     # ....backward path...for acks
#     rdt_receiver.channel = channel_for_ack
#     channel_for_ack.receiver = rdt_sender

#     # Run simulation
#     env.run(until=receiving_app.isCompleted)
#     current_t_avg = float('inf')
#     if len(rdt_sender.rtt) > 0:
#         current_t_avg = sum(rdt_sender.rtt)/len(rdt_sender.rtt)
#     t_avgs.append(current_t_avg)
#     print("T_avg:", current_t_avg)

# # plot the results
# plt.plot(t_avgs)
# plt.xlabel("Pc")
# plt.ylabel("T_avg")

# # beautify plot
# # plt.xticks(np.arange(0,0.9,0.1))


# plt.show()


