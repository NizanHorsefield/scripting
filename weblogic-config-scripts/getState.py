#vars from props file
#adminURL=configProps.get("admin.url")
#adminUserName=configProps.get("admin.userName")
#adminPassword=configProps.get("admin.password")

#testing vars
adminURL="t3://sit1-evise-wc-adminserver.evise-cloud.com:7001"
adminUserName="weblogic"
adminPassword="getrdone1"

#redirect wlst's own output to null, print lines in the script itself
redirect('/dev/null', 'false')
 
#connect(userConfigFile='/home/weblogic/user_projects/domains/my_domain/adminServerConfig.secure',
#        userKeyFile='/home/weblogic/user_projects/domains/my_domain/adminServerKey.secure',
#        url='t3://myhost.mydomain.ie:7001')

connect(adminUserName, adminPassword, adminURL)
 
servers = cmo.getServers()
 
domainRuntime()
stoppedServers = []
 
for server in servers:
    try:
        cd('/ServerRuntimes/' + server.getName())
        currentState = get('HealthState').getState()
        if currentState == 0:
            print server.getName() + ': ' + get('State') + ': HEALTH_OK'
        elif currentState == 1:
            print server.getName() + ': ' + get('State') + ': HEALTH_WARN'
        elif currentState == 2:
            print server.getName() + ': ' + get('State') + ': HEALTH_CRITICAL'
            stoppedServers.append(server.getName())
        elif currentState == 3:
            print server.getName() + ': ' + get('State') + ': HEALTH_FAILED'
            stoppedServers.append(server.getName())
        elif currentState == 4:
            print server.getName() + ': ' + get('State') + ': HEALTH_OVERLOADED'
        else:
            print server.getName() + ': ' + get('State') + ': UNKNOWN HEALTH STATE (' + currentState + ')'
 
    except WLSTException, e:
        print server.getName() + " is not running."
        stoppedServers.append(server.getName())
 
disconnect()