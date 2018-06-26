import sys;

connect('lifecycle','Password123','t3://localhost:7001')
#connect('weblogic','weblogic1','t3://localhost:7001'

server = sys.argv[1]

print "Starting nexteesadf_server" + server
start('nexteesadf_server' + server,'Server')
