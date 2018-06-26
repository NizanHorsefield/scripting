import socket;
admin_server_listen_address = socket.gethostname();
admin_server_url = 't3://' + admin_server_listen_address + ':' + admin_server_listen_port;
 
print 'CONNECT TO ADMIN SERVER';
connect(admin_username, admin_password, admin_server_url);
 
print 'STOP MANAGED SERVERS';
domainRuntime();
server_lifecycles = cmo.getServerLifeCycleRuntimes();
 
for server_lifecycle in server_lifecycles:
    if (server_lifecycle.getState() == 'RUNNING' and server_lifecycle.getName() != admin_server_name):
        print 'STOP SERVER ' + server_lifecycle.getName();
        task = server_lifecycle.shutdown(1000, java.lang.Boolean('true'));
        while (task.isRunning() == 1):
            print 'STOPPING SERVER ' + server_lifecycle.getName();
            java.lang.Thread.sleep(2000);
        print 'SERVER ' + server_lifecycle.getName() + ' is in ' + server_lifecycle.getState() + ' state';
    else:
        print 'SERVER ' + server_lifecycle.getName() + ' is in ' + server_lifecycle.getState() + ' state and will not be stopped';
 
print 'DISCONNECT FROM THE ADMIN SERVER';
disconnect();