#!/usr/bin/env python
import socket
import struct
import sys
import time

import json
import urllib2

import struct


message = 'very important data'
multicast_group = '239.255.52.100'
PORT=7000
server_address = ('', PORT)

STATS_INTERVAL = 1
HELLO_URL = "http://mcastserver:7001/hello"
STATS_URL = "http://mcastserver:7001/send_stats"

def parse(packet):
    id = ord(packet[3])
    ts = packet[4:8]
    us = packet[8:12]
    ts = struct.unpack(">L", ts)[0]
    us = struct.unpack(">L", us)[0]
    return ts, us, id
    

def recv(seconds=4):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    sock.settimeout(seconds)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print "waiting for first packet..."
    data, address = sock.recvfrom(1024*64)
    print "got it. Testing for %d seconds" % seconds

    start = c = s = time.time()
    dups = packets = total = 0
    idx = 1
    last = (0,0,0)
    while c - start < seconds:
        data, address = sock.recvfrom(1024*64)
        info = parse(data)
        if not info > last:
            dups += 1
        else :
            packets += 1
            total += len(data)
            last = info
        c = time.time()
        if c- s >= STATS_INTERVAL:
            kbytes = total/1024
            mbit = kbytes*8/1024.0/STATS_INTERVAL
            packets_sec = packets / STATS_INTERVAL

            a_time = info[0] + info[1] / 1000000.0
            delay = c - a_time
            yield dict(time=c, kbytes=kbytes, mbits=mbit, pps=packets_sec, dups=dups, delay=delay, interval=STATS_INTERVAL, idx=idx)

            dups = total = packets = 0
            s=c
            idx += 1

def send_hello():
    for x in range(5):
        try :
            return urllib2.urlopen(HELLO_URL, timeout=10).read()
        except Exception, e:
            time.sleep(1)

def send_stats(items):
    print "Uploading results to server..."
    data = json.dumps(items)
    for x in range(5):
        try :
            urllib2.urlopen(STATS_URL, data, timeout=10).read()
            print "Sent!"
            return True
        except Exception, e:
            print e
            time.sleep(2)

def run_test(seconds):
    print "Server says:", send_hello()
    items = []
    try :
        for stat in recv(seconds):
            items.append(stat)
            print "%(idx)3d %(time)s %(kbytes)d Kbytes %(interval)0.2f seconds %(mbits)0.2f megabit %(pps)0.2f pps %(dups)d dups %(delay)0.3f delay" % (stat)
    finally:
        send_stats(items)

if __name__ == "__main__":
    import sys
    seconds = 60
    try :
        seconds = int(sys.argv[1])
    except:
        pass
    run_test(seconds)
