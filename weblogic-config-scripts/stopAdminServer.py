import socket;
node_manager_listen_address = socket.gethostname();
admin_server_listen_address = node_manager_listen_address;
admin_server_url = 't3://' + admin_server_listen_address + ':' + admin_server_listen_port;
 
print 'CONNECT TO ADMIN SERVER';
connect(admin_username, admin_password, admin_server_url);
 
print 'CONNECT TO NODE MANAGER';
nmConnect(node_manager_username, node_manager_password, node_manager_listen_address, node_manager_listen_port, domain_name, domain_home, node_manager_mode);
 
print 'STOPPING ADMIN SERVER';
shutdown(admin_server_name,'Server','true',1000,'true');
 
print 'DISCONNECT FROM NODE MANAGER';
nmDisconnect();