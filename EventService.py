import os
import string
import sys
import time
from random import randint
from threading import Thread

eventServiceIP=""#holds ip of event service
eventServicePort=""# holds port

class EventService:
	def __init__(self, callback):
		self.callback = callback

	def subscribeMsg(ip,port,topic,msg):
		xpub_url="tcp://"+ip+":"+port
		ctx = zmq.Context()
		sub = ctx.socket(zmq.SUB)
		sub.connect(xpub_url)
		topics = 'AAA'
		subscription = set()
		while True:
			r = randint(0,len(topics))
			if r < len(topics):
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
			OnMsgRecieve(topic, list1)

			list1.sort()     	
					for x in list1: 
					print "received", x
			print "for the message %s with priority %s" % (x[0], x[1]), "process time in subscriber is", time.clock()
				else:
					break
					
		def publishMsg(topic,ip,port,msg):
			url="tcp://"+ip+":"+port
			context = zmq.Context()
			socket = context.socket(zmq.PUB)
			socket.connect(url)
			# pub.bind(xpub_url)
			for n in range(1000):
				for topic in "ABC":
					priority=randint(0,9)
					msg = [topic, str(priority), str(n)]
					socket.send_multipart(msg)
					print "for the message %s with priority %d" % (topic, priority), "process time in publisher is", time.clock()
				time.sleep(0.25)
				
		def OnMsgRecieve(topic, msg):
			msg.sort()     	
					for x in msg: 
					print "received", x
			print "for the message %s with priority %s" % (x[0], x[1]), "process time in subscriber is", time.clock()
		
		callback #how does this need to be called exactly
			