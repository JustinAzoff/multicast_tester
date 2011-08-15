#!/bin/sh -x 
iperf -c 239.255.52.100  -u -T 3  -t 30 -i 1 -b 20m -p 7000
