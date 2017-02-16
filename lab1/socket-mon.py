import psutil
# print psutil.net_connections()
list = psutil.net_connections()
print "pid,laddr,raddr,status"
for item  in list:
    print item
    if len(item.laddr) >= 2 and len(item.raddr) >= 2:
        # print item.raddr
        print "%r, %r, %r, %r" % (item.pid , str(item.laddr[0]) + '@' + str(item.laddr[1]) , str(item.raddr[0]) + '@' + str(item.raddr[1]) , item.status)
