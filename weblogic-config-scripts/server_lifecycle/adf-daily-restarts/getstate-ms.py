import sys;

connect('weblogic','weblogic1','t3://localhost:7001')

server = sys.argv[1]

print "Starting nexteesadf_server" + server
state('nexteesadf_server' + server,'Server')
