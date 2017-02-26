import hashlib
from hash_ring import HashRing
from Net import Net
import sys
from threading import Thread
import time
class Finger:
    def __init__(self):
        self.succssor = 0
        self.ip = ""


class ChordNode:
    def __init__(self):
        if len(sys.argv) >= 2:
            self.ip = sys.argv[1]
        else:
            self.ip = "127.0.0.1"
        self.listID = []
        for i in range(0, 256):
            self.listID.append(i)
        self.id = self.hash()
        print "Initialize ChordNode", self.id
        self.successor = self.id
        self.successor_ip = self.ip
        self.predecessor = self.id
        self.predecessor_ip = self.ip
        self.m = 8
        self.finger = {}
        self.init_finger_table()
        self.net = Net(self.ip, callbackMsgRcvd=self.message_received)
        self.next = -1

        if len(sys.argv) >= 3:
            self.start_mode = "join"
            self.join_ip = sys.argv[2]
            print "start_mode:", self.start_mode, "join_ip", self.join_ip
        else:
            self.start_mode = "create"

        if self.start_mode == "join":
            self.join()
        else:
            self.successor = self.id

        t = Thread(target=self.fix_fingers)
        t.start()

    def join(self):
        print "joining to", self.join_ip
        s, self.successor_ip = self.call_remote_proc(self.join_ip, "findSuccessor", str(self.id)).split()
        self.successor = int(s)

        p, self.predecessor_ip = self.call_remote_proc(self.successor_ip, "getPredecessor", "NONE").split()
        self.predecessor = int(p)

        self.call_remote_proc(self.predecessor_ip, "updateSuccessor", str(self.id) + "," + self.ip)
        self.call_remote_proc(self.successor_ip, "updatePredecessor", str(self.id) + "," + self.ip)

    def fix_fingers(self):
        time.sleep(3)
        while True:
            time.sleep(3)
            self.next += 1
            if self.next >= self.m:
                self.next = 0
            print "fix_fingers", self.next, "s:",self.successor, "p:", self.predecessor
            s = self.find_successor((self.id + 2**(self.next))%256)
            print "fix_fingers", self.next, " rcvd s:", s
            self.finger[self.next].successor,self.finger[self.next].ip = s.split()
            print "fix_fingers fixed to ", self.finger[self.next].ip
            for i in range(0, len(self.finger)):
                print i, " --- ", (self.id + 2**(i))%256, " --- ", self.finger[i].successor, " --- ", self.finger[i].ip
    def message_received(self, msg):
        print "New msg arrived", "msg:", msg
        topic,data = msg.split()
        if topic == "findSuccessor":
            return self.find_successor(int(data))
        if topic == "getPredecessor":
            return str(self.predecessor) + " " + self.predecessor_ip
        if topic == "updateSuccessor":
            s, self.successor_ip = data.split(",")
            self.successor = int(s)
            return data
        if topic == "updatePredecessor":
            p, self.predecessor_ip = data.split(",")
            self.predecessor = int(p)
            return data
        return "0"

    def init_finger_table(self):
        for i in range(0, self.m):
            f = Finger()
            f.successor = self.id
            f.ip = self.getIP()
            self.finger[i] = f

    def find_successor(self, id):
        print "find_successor called for ", id, "self.successor", self.successor
        if id < self.id:
            id = id + 256
        if self.id > self.successor and id in range(self.id, 256+self.successor):
            return str(self.successor) +" "+self.successor_ip
        elif id in range(self.id, self.successor):
            return str(self.successor) +" "+self.successor_ip
        else:
            n = self.closest_preceding_node(id)
            if n is None:
                return str(self.id) + " " + self.ip
            if n.successor == self.id:
                return str(self.id) + " " + self.ip
            if n.successor == self.successor:
                return str(self.id) + " " + self.ip
            return self.call_remote_proc(n.ip, "findSuccessor", str(id))

    def closest_preceding_node(self, id):
        for i in range(self.m-1, -1, -1):
            print "closest_preceding_node, i:", i
            if self.id > id and self.finger[i].successor in range(self.id , 256+id+1):
                return self.finger[i]
            elif self.finger[i].successor in range(self.id, id+1):
                return self.finger[i]
        return None

    def call_remote_proc(self, ip, proc, data):
        print "Calling remote proc of ", ip, " proc", proc, "with data:", data
        ret_msg = self.net.call_remote_procedure(ip, proc, data)
        print "rcvd msg from RPC: ", ip, " proc", proc, "with data:", data, "rcvd:", ret_msg
        return ret_msg

    def hash(self):
        ring = HashRing(self.listID)
        id = ring.get_node(self.getIP())
        return id

    def getIP(self):
        return self.ip


ChordNode()
