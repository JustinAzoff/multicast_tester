this is a working but incomplete multicast tester.

it uses iperf on the server and python on the client.

the client tests the performance and uploads the data back to the server.

How to use
==========

Run on the server:

    ./manage_iperf.py
    ./run_web

then on the clients:

    ./receive.py server.ip.address 300
