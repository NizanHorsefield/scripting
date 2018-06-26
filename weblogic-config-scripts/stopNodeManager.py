import socket;
node_manager_listen_address = socket.gethostname();
 
nmConnect(node_manager_username, node_manager_password, node_manager_listen_address, node_manager_listen_port, domain_name, domain_home, node_manager_mode);
stopNodeManager();