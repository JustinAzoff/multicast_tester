#!/bin/sh -x 
iperf -c 239.255.52.100  -u -T 3  -i 1 -b 100m -p 7000
