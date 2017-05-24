# encoding: utf-8
 
import zlib
 
"""
copy from:
https://github.com/afirel/consistent_hashr/blob/master/lib/consistent_hashr.rb
http://www.tom-e-white.com/2007/11/consistent-hashing.html
"""
class ConsistentHash(object):
    def __init__(self, replicas, servers):
        self.replicas = replicas
        self.circle = {}
        for server in servers:
            self.add(server)
 
    @staticmethod
    def _hash(server, idx):
        return zlib.crc32(server + ":" + str(idx))
 
    def add(self, server):
        for x in range(0, self.replicas):
            self.circle[ConsistentHash._hash(server, x)] = server
 
    def remove(self, server):
        for x in range(0, self.replicas):
            hsh = ConsistentHash._hash(server, x)
            if self.circle.get(hsh):
                del self.circle[hsh]
 
    def get(self, key):
        if not self.circle:
            return None
        hsh = zlib.crc32(key)
        largers = filter(lambda x: x >= hsh, self.circle.keys())
 
        def first_server(hashes):
            """
             first server whose hash bigger than hash
            """
            hashes = sorted(hashes)
            return self.circle[hashes[0]]
        return first_server(largers) if largers else first_server(self.circle.keys())
 
 
if __name__ == "__main__":
    h = ConsistentHash(10, ["192.168.65.53", "192.168.65.101", "192.168.65.808"])
    print(h.get("554"))
    h.add("192.168.65.54")
    print(h.get("554"))
    h.remove("192.168.65.101")
    print(h.get("554"))
    h.remove("192.168.65.100")
    print(h.get("554"))