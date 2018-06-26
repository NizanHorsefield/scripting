import sys
from java.io import FileInputStream

# Import the property file
# propInputStream = FileInputStream("../conf/sit1.properties") # use if a dir scaffold is in place
propInputStream = FileInputStream(sys.argv[1])
configProps = Properties()
configProps.load(propInputStream)

#vars from props file
adminURL=configProps.get("admin.url")
adminUserName=configProps.get("monitor.userName")
adminPassword=configProps.get("monitor.password")

#redirect wlst's own output to null, print lines in the script itself
redirect('/dev/null', 'false')

# connect to the admin server
connect(adminUserName, adminPassword, adminURL)
# move to the domain runtime
domainRuntime()
server = sys.argv[2]

# get list of servers that are running
def getRunningServerList():
    runningList = [];
    serverlist=cmo.getServers()
    for s in serverlist:
        serverName = s.getName()
        cd("/ServerLifeCycleRuntimes/" + serverName)
        serverState = cmo.getState()
        if serverState == 'RUNNING':
            runningList.append(serverName)

    


#get state of JVM
def getState(jvm):
    try:
        cd('/ServerRuntimes/' + jvm)
        jvmstate = cmo.getState()
        if jvmstate == 'RUNNING':
            return 1
        else:
            return 0
    except WLSTException, err:
        print(err)

# get Hogging Thread Count
def getHTC(jvm):
    try:
        cd('/ServerRuntimes/' + jvm + '/ThreadPoolRuntime/ThreadPoolRuntime')
        hoggerthreadcount = cmo.getHoggingThreadCount()
        return str(hoggerthreadcount)
    except WLSTException, err:
        print(err)

        # get STUCK thread counts
def getSTC(jvm):

    try:
        cd('/ServerRuntimes/' + jvm)
        #servers = ls('/ServerRuntimes','true','c')

        # store all results in a dictionary, using the server name for a key
        result=dict()
        deployments = ls('/ServerRuntimes/' + jvm + '/ApplicationRuntimes','true','c')
        result[jvm] = 0;
        for deployment in deployments:
            ## if only a single deployment:
            ## if(deployment.getName() == "MyApplication"):

            ## if multiple workmanagers:
            wms = ls('/ServerRuntimes/'  + jvm + '/ApplicationRuntimes/' \
                     + deployment + '/WorkManagerRuntimes','true','c')
            for wm in wms:
                cd('/ServerRuntimes/' + jvm + '/ApplicationRuntimes/' \
                   + deployment + '/WorkManagerRuntimes/' + wm)
                result[jvm] = result[jvm] + get('StuckThreadCount')
        for key in result:
            return(str(result[key]))
    except WLSTException, err:
        print(err)
        
## Reenable printing output
redirect('/dev/null','true')

# get JDBC Runtime Metrics
def getJdbcMetrics(jvm):

    try:
        jdbcRuntime = jvm.getJDBCServiceRuntime();
        datasources = jdbcRuntime.getJDBCDataSourceRuntimeMBeans();
        for datasource in datasources:
            print('-Data Source: ' + datasource.getName() + ', Active Connections: ' + repr(datasource.getActiveConnectionsCurrentCount()) + ', Waiting for Connections: ' + repr(datasource.getWaitingForConnectionCurrentCount()));
    except WLSTException, err:
        print(err)

# get HEAP free %
def getHeapFreePercent(jvm):
    try:
        cd('/ServerRuntimes/' + jvm + '/JVMRuntime/' + jvm)
        heapfreepercent = cmo.getHeapFreePercent()
        return str(heapfreepercent)
    except WLSTException, err:
        print(err)

# Run the collection methods:
htc = getHTC(server)
stc = getSTC(server)
#getJdbcMetrics()
heap = getHeapFreePercent(server)
state = getState(server)

#Create the return string
metricResult = 'jvmmetrics,' + htc + ',' + stc + ',' + heap + ',' +str(state)

#Return the string
print metricResult

#Disconnect from the Admin server.
disconnect()
