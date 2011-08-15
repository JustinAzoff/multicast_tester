#!/usr/bin/env python
import socket
import struct
import sys
import time
import threading
import Queue

message = 'very important data'
multicast_group = '239.255.52.100'
PORT=7000
server_address = ('', PORT)
STATS_INTERVAL = 1

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
    while c - start < seconds:
        data, address = sock.recvfrom(8192)
        total += len(data)
        c = time.time()
        if c- s >= STATS_INTERVAL:
            kbytes = total/1024
            mbit = kbytes*8/1024.0/STATS_INTERVAL

            yield c, kbytes, mbit

            total=0
            s=c

def send_stats(item):
    print "%s %d Kbytes in %0.2f seconds %0.2f megabit" % (item[0], item[1], STATS_INTERVAL, item[2])

def stats_thread(Q):
    while True:
        item = Q.get()
        if item is None:
            return
        send_stats(item)

def run_test(seconds):
    for x in recv(seconds):
        send_stats(x)

if __name__ == "__main__":
    import sys
    seconds = 30
    try :
        seconds = int(sys.argv[1])
    except:
        pass
    run_test(seconds)
