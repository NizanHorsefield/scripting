import socket;
admin_server_listen_address = socket.gethostname();
admin_server_url = 't3://' + admin_server_listen_address + ':' + admin_server_listen_port;
 
print 'CONNECT TO ADMIN SERVER';
connect(admin_username, admin_password, admin_server_url);
 
all_servers = cmo.getServers();
servers = [];
for server in all_servers:
    if (server.getName() != 'AdminServer' and server.getCluster() is not None):
        servers.append(server);
 
machines = cmo.getMachines();
for machine in machines:
    node_manager_listen_address = machine.getNodeManager().getListenAddress();
    node_manager_listen_port = machine.getNodeManager().getListenPort();
    print 'CONNECT TO NODE MANAGER ON ' + node_manager_listen_address + ':' + repr(node_manager_listen_port);
    nmConnect(node_manager_username, node_manager_password, node_manager_listen_address, node_manager_listen_port, domain_name, domain_home, 'ssl');
    for server in servers:
        if (node_manager_listen_address == server.getListenAddress()):
            print 'STARTING SERVER ' + server.getName();
            start(server.getName(),'Server');
    print 'DISCONNECT FROM NODE MANAGER ON ' + node_manager_listen_address + ':' + repr(node_manager_listen_port);
    nmDisconnect();
 
print 'DISCONNECT FROM THE ADMIN SERVER';
disconnect();
