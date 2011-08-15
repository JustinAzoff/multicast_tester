#!/usr/bin/env python
import socket
import struct
import sys
import time

message = 'very important data'
multicast_group = '239.255.52.100'
PORT=7000
server_address = ('', PORT)

def send():
    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)

    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 3)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    while True:
        sent = sock.sendto(message, (multicast_group, PORT))
        time.sleep(1)

def recv(seconds=4):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    sock.settimeout(seconds)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print "waiting for first packet..."
    data, address = sock.recvfrom(8192)
    print "got it. Testing for %d seconds" % seconds

    start = c = s = time.time()
    total = 0
    all_total = 0
    while c - start < seconds:
        data, address = sock.recvfrom(8192)
        total += len(data)
        all_total += len(data)
        c = time.time()
        if c- s >= 1:
            kbytes = total/1024
            mbit = kbytes*8/1024.0
            if kbytes > 2:
                print "%d Kbytes in %0.2f seconds %0.2f megabit" % (kbytes, c-s, mbit)
            total=0
            s=c

    kbytes = all_total/1024
    mbit = kbytes*8/1024.0/(c-start)
    print "%d Kbytes in %0.2f seconds %0.2f megabit" % (kbytes, c-start, mbit)

if __name__ == "__main__":
    import sys
    seconds = int(sys.argv[1])
    recv(seconds)
