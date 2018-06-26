import socket;
# socket.gethostbyaddr(socket.gethostbyname(socket.gethostname()))[0] or socket.getfqdn() for short obtains the fully qualified domain name
# more information on using socket can be found in the following link: http://docs.python.org/2/library/socket.html
node_manager_listen_address = socket.gethostname();
 
startNodeManager(verbose='true', NodeManagerHome=node_manager_home, ListenPort=node_manager_listen_port, ListenAddress=node_manager_listen_address);