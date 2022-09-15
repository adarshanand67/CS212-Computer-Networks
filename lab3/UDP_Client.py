# This is the client program that uses UDP

# Sequence:
#
# 1. Create a socket
# 2. Send messages to it
# (We need to know the server's hostname and port.)

import socket

# create a socket
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# The first argument should be AF_INET
	# The second argument is SOCK_STREAM for TCP service
	#    and SOCK_DGRAM for UDP service

host='localhost'
# host = '10.196.9.75'
port=43387  # this is the server's port number, which the client needs to know

# send some bytes (encode the string into Bytes first)
message = "I could tell you a UDP joke but I'm not sure you'll get it."
s.sendto( message.encode('utf-8'), (host,port))


# see if the other side responds
data, addr = s.recvfrom(1024) # buffer size is 1024 bytes
print("Client received MESSAGE=",data.decode()," from ADDR=",addr)

# close the connection
s.close()
