
# Uses XPUB subscription messages to re-send data when we get new subscriber
#

import zmq

def main():
    ctx = zmq.Context.instance()
    subscriber = ctx.socket(zmq.SUB)
    subscriber.connect("tcp://127.0.0.1:5556")
    publisher = ctx.socket(zmq.XPUB)
    publisher.bind("tcp://127.0.0.1:5555")

    # We Subscribe to every single topic from publisher
    subscriber.setsockopt(zmq.SUBSCRIBE, b"")

    # We store last instance of each topic and we can use list and store many of them
    listing = {}

    
    
    poller = zmq.Poller()
    poller.register(subscriber, zmq.POLLIN)
    poller.register(publisher, zmq.POLLIN)
    while True:

        try:
            events = dict(poller.poll(1000))
        except KeyboardInterrupt:
            print("poll interruption occured")
            break

        # When new topic comes we store it and forward for subscribers
        if subscriber in events:
            message = subscriber.recv_multipart()
            topic, current = message
            listing[topic] = current
            publisher.send_multipart(message)

        # We are checking the new subscribers
        # When we get a new subscriber request we are getting the data and send it to subscriber:
        if publisher in events:
            message = publisher.recv()
            # if the event gets 0 it means unsubscribe, if 1 it means subscribe
            if message[0] == b'\x01':
                topic = message[1:]
                if topic in listing:
                    print ("Sending the topic that is stored for new subscriber %s" % topic)
                    publisher.send_multipart([ topic, listing[topic] ])

if __name__ == '__main__':
    main()
