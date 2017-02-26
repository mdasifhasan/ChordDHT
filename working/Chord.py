import hashlib
from hash_ring import HashRing
from Net import Net
import sys


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
        for i in range(0, 128):
            self.listID.append(i)
        self.id = self.hash()
        print "Initialize ChordNode", self.id
        self.successor = self.id
        self.predecessor = None
        self.m = 128
        self.finger = {}
        self.init_finger_table()
        self.net = Net(self.ip, callbackMsgRcvd=self.message_received)

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

    def join(self):
        print "joining to", self.join_ip
        self.successor = self.call_remote_proc(self.join_ip, "findSuccessor", str(self.id))

    def message_received(self, msg):
        print "New msg arrived", "msg:", msg
        topic,data = msg.split()
        if topic == "findSuccessor":
            return self.find_successor(data)
        return "0"

    def init_finger_table(self):
        for i in range(0, self.m):
            f = Finger()
            f.successor = self.id
            f.ip = self.getIP()
            self.finger[i] = f

    def find_successor(self, id):
        if id in range(self.id, self.successor):
            return self.ip
        else:
            n = self.closest_preceding_node(id)
            if n == None:
                return self.ip
            return self.call_remote_proc(n.ip, "findSuccessor", str(id))

    def closest_preceding_node(self, id):
        for i in range(self.m-1, -1):
            if self.finger[i].successor in range(self.id, id+1):
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
