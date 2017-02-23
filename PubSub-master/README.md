# PubSub
PubSub
## Explanation
In our program, we are creating Subscriber, Publisher, Intermediary and Fault Tolerance.
Also, we are defining the OwnershipStrength beginning from 0 to 9. It means, the topic which have 0 OwnershipStrength will be the very first that is sent to subscriber. We have taken our results in terms of Publisher, Subscriber and Intermediary. We are recording the clock time of topics that are sent by publishers in publisher data. And also we keep track of the binding records in intermediary by looking at their arrival time. And we are sorting the ownership strengths in Intermediary and send the topics according to that sorting to our Subscribers. In Fault Tolerance, when we have new subscriber, We are keeping the last value caches and when a new subscriber connects having b'\x01': in its record. It means new subscriber is connected. And We are sending the last value in cache. We have created a custom topology that you can see in the code but it can work the other topologies We think

