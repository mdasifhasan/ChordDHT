"""
An PubSub Intermediary that is working like an intermediate listener
"""
import os
import string
import sys
import time
from random import randint
from threading import Thread
import Queue
import zmq

list2=[]


xpub_url = "tcp://127.0.0.1:5555"
xsub_url = "tcp://127.0.0.1:5556"
list1=[]
def broker():
    ctx = zmq.Context()
    xpub = ctx.socket(zmq.XPUB)
    xpub.bind(xpub_url)
    xsub = ctx.socket(zmq.XSUB)
    xsub.bind(xsub_url)
    
    poller = zmq.Poller()
    poller.register(xpub, zmq.POLLIN)
    poller.register(xsub, zmq.POLLIN)


    while True:
        events = dict(poller.poll(1000))
        if xpub in events:
	    message=xpub.recv_multipart()
	    list2.append(message)
            if message[0] == b'\x01':
                topic = message[1:]
                if topic in list2:
                    print "Sending cached topic %s",   topic
                    xpub.send_multipart(topic) 		
	    for n in range(30):
   		list1.append(message)
	    list1.sort()     
	    
            print "[BROKER] subscription message: %r" % message[0]
	    
	    for x in list1:    
            	xsub.send_multipart(x)
		print "process time of",x,"in intermediary is", time.clock()	
	       
            	

	
   
        if xsub in events:
            message = xsub.recv_multipart()
	    list2.append(message)
	    
	    for n in range(30):
   		list1.append(message)
	
	    list1.sort()  
           
	    for x in list1: 
            	xpub.send_multipart(x)
		print "process time of",x,"in intermediary is", time.clock()



if __name__ == '__main__':
    ctx = zmq.Context()
    broker()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    "terminating"
    ctx.term()
    [ t.join() for t in threads ]