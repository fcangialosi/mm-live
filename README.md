mm-live
=======

Live plotting for [mahimahi](https://github.com/ravinet/mahimahi/). Mahimahi
comes with a very nice live plotting system already, but unfortunately it does
not work over ssh, which is the main context in which I use mahimahi. This
system fills that void by creating a server that any number of clients can
connect to simultaneously through their web browser. The server pushes the raw
throughput and delay data to the clients using websockets and the browser plots
the data using d3. 

Usage
=====

To live plot the throughput and delay of any mahimahi shell, simply add
`mm-live` as the outer-most shell.

For example, to start a server with 50ms delay, 48Mbps bandwidth, and 1BDP
droptail buffers, with live plotting:

`mm-live mm-delay 25 mm-link --uplink-queue="droptail" --uplink-queue-args="packets=100" --uplink-log=test.log ~/bw12.mahi ~/bw48.mahi`

This will create a server on port 8088. If the ip address of your server is
1.2.3.4, you can view it from the following URL in your browser:

1.2.3.4:8088/

Dependencies
============

(Instructions assume all of these are already installed in the typical
locations):

* Node.js
* Python
* Mahimahi

