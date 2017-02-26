import hashlib
from hash_ring import HashRing
class ChordNode:
    def __init__(self):
        self.listID = []
        for i in range (0,128):
            self.listID.append(i)
        self.id = self.hash()
        print "Initialize ChordNode", self.id
        self.successor = self.id
        self.predecessor = None
        self.finger = {}
        self.m = 128

    def find_successor(self, id):
        if id in range(self.id, self.successor):
            return self.successor
        else:
            n = self.closestPrecedingNode(id)
            return self.callRemoteProc(n, "findSuccessor", [id])

    def closest_preceding_node(self, id):
        for i in range(self.m, 0):
            if self.finger[i] in range(self.id, id):
                return self.finger[i]
        return self.id

    def call_remote_proc(self, id, proc, args):
        print "Calling remote proc of ", id, " proc", proc, "with args:", args

    def hash(self):
        ring = HashRing(self.listID)
        server = ring.get_node('192.168.1.243')
        return server
ChordNode()