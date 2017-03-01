# ChordDHT

1. Create mininet network using a command such as "sudo mn --top=tree, depth=1, fanout=10"
2. Create first node "xterm h1"
3. Start the event service and pass in the host Ip address. "python eventService.py 10.0.0.1"
4. A virtual id will be assigned.
5. Other nodes following steps 2 and 3 adjusting arguments to the new values. When repeating step 3 the arguments are the new nodes ip as well as any node ip already in the network that you wish to connect to.
6.continue as much as you wish
7. create a new node
8. run suscribe.py in the new node passing the IP of node in the network and a topic as command line arguments respectively.
9. continue as much as you wish
10. for publisher create a new node.
11. run publisher.py with the query node ip and the topic it wishes to publish about as command-line arguments respectively this will cause it to publish. subscribers with that topic will get messages.
