loadProperties('props.properties')
## props.properties
# SERVERS=myser1,myser2,myser3;myser4,myser5,myser6
# ADMINSERVER=demoAdmin
##

print SERVERS
print '################'
serverlist=SERVERS.split(';')
print '################'
for i in serverlist:
    j=i.split(',')
    print j
    for k in j:
        print k
print '################'
