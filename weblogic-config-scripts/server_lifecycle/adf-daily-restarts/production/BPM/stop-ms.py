gimport sys;
connect('lifecycle','L1f3cycl3!','t3://prod-evise-soa1-adminserver.evise-cloud.com:7001')
server = sys.argv[1]
shutdown('soa_server' + server,'Server','false',2400,block='false')

