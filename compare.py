from System import *
from com.google.common.collect.Lists import *
from com.google.common.collect.Maps import *
from com.google.common.hash.Funnel import *
from com.google.common.hash.Funnels import *
from com.google.common.hash.HashFunction import *
from com.google.common.hash.Hashing import *
from System.Collections.Concurrent import *
from System.Collections.Generic import *
from System.Collections import *
from System.IO import *
from System.Threading import *
# *
# * For comparing the load differences between consistent hash and HRW
# 
class Compare(object):
	def __init__(self):
		self._hfunc = Hashing.murmur3_128()
		self._strFunnel = Funnels.stringFunnel(Charset.defaultCharset())

	def main(args):
		distribution = Maps.newHashMap()
		Console.WriteLine("======: ConsistentHash :========")
		c = ConsistentHash(self._hfunc, self._strFunnel, self._strFunnel, Compare.getNodes(distribution))
		i = 0
		while i < 10000:
			distribution.get(c.get("" + i)).incrementAndGet()
			i += 1
		while :

	main = staticmethod(main)