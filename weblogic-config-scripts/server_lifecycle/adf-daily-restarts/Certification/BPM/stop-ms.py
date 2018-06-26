import sys;
connect('lifecycle','L1f3cycl3!','t3://cert-evise-soa1-adminserver.evise-cloud.com:7001')
server = sys.argv[1]
shutdown('soa_server' + server,'Server','false',1200,block='false')

