#!/usr/bin/env python
import socket
import struct
import sys
import time

import json
import urllib2

import struct

multicast_group = '239.255.52.100'
PORT=7000
server_address = ('', PORT)

STATS_INTERVAL = 1
HELLO_URL = "http://mcastserver:7001/hello"
STATS_URL = "http://mcastserver:7001/send_stats"

def parse(packet):
    id = packet[0:4]
    ts = packet[4:8]
    us = packet[8:12]
    ts = struct.unpack(">L", ts)[0]
    us = struct.unpack(">L", us)[0]
    id = struct.unpack(">l", id)[0]
    net_time = ts + us/1000000.0
    return net_time, id
    

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
    info = parse(data)
    net_time = info[0]

    start = c = s = net_time
    loss = dups = packets = total = 0
    idx = 1
    last = info
    last_seq = info[1]
    while net_time - start < seconds:
        data, address = sock.recvfrom(1024*64)
        info = parse(data)
        if not info > last:
            dups += 1
        else :
            packets += 1
            total += len(data)
            last = info
            #calculate loss
            seq = info[1]
            diff = seq - (last_seq + 1 )  
            #wrap around should be impossible now.. iperf would need to be running for 5 days
            if diff > 0:
                loss += diff
            last_seq = seq

        net_time = info[0]
        if net_time - s >= STATS_INTERVAL:
            kbytes = total/1024
            mbit = kbytes*8/1024.0/(net_time - s)
            packets_sec = packets / (net_time - s)
            loss_pct = 100.0 * loss/(loss+packets)

            c = time.time()
            delay = c - net_time
            yield dict(time=c, kbytes=kbytes, mbits=mbit, pps=packets_sec, dups=dups, delay=delay, loss=loss_pct, interval=STATS_INTERVAL, idx=idx)

            loss = dups = total = packets = 0
            s=net_time
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
            print "%(idx)3d %(time)s %(kbytes)d Kbytes %(interval)0.2f seconds %(mbits)0.2f megabit %(pps)0.2f pps %(dups)d dups %(delay)0.3f delay %(loss).1f loss" % (stat)
    except Exception, e:
        print e
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
