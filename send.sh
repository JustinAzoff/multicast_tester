#!/bin/sh -x 
while true; do
    iperf -c 239.255.52.100 -t 3600 -u -T 3  -i 1 -b 100m -p 7000
done
