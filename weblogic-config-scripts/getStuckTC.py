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
	cd('ThreadPoolRuntime/ThreadPoolRuntime')
	hoggerTC = cmo.getHoggingThreadCount()
	print server.getName() + ' : HTC : ' + str(hoggerTC)
 
    except WLSTException, e:
        print "Could not get HTC for " + server.getName()
 
disconnect()
