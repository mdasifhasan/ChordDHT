import os
import string
import sys

from threading import Thread
import time
from random import randint
import zmq

xpub_url = "tcp://127.0.0.1:5555"
xsub_url = "tcp://127.0.0.1:5556"
count=1
list1=[]
def subscriber():
    ctx = zmq.Context()
    sub = ctx.socket(zmq.SUB)
    sub.connect(xpub_url)
    topics = 'AAA'
    subscription = set()
    while True:
        r = randint(0,len(topics))
        if r < len(topics):
            topic = topics[r]
            if topic not in subscription:
                subscription.add(topic)
                sub.setsockopt(zmq.SUBSCRIBE, topic)
        r2 = randint(0,len(topics))
        if r2 != r and r2 < len(topics):
            topic = topics[r2]
            if topic in subscription:
                subscription.remove(topic)
                sub.setsockopt(zmq.UNSUBSCRIBE, topic)
        time.sleep(0.3)
        
        while True:
            if sub.poll(timeout=0):
		for n in range(20):
   		    list1.append(sub.recv_multipart())

		list1.sort()     	
                for x in list1: 
                   print "received", x
		   print "for the message %s with priority %s" % (x[0], x[1]), "process time in subscriber is", time.clock()
            else:
                break
if __name__ == '__main__':
    subscriber()
    
