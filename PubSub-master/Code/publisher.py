import os
import string
import sys
import time
from random import randint
from threading import Thread

import zmq

xpub_url = "tcp://127.0.0.1:5555"
xsub_url = "tcp://127.0.0.1:5556"
context = zmq.Context()


socket = context.socket(zmq.PUB)
socket.connect(xsub_url)
# pub.bind(xpub_url)
for n in range(1000):
   for topic in "ABC":
       priority=randint(0,9)
       msg = [topic, str(priority), str(n)]
       socket.send_multipart(msg)
       print "for the message %s with priority %d" % (topic, priority), "process time in publisher is", time.clock()
       
       
   time.sleep(0.25)
    


