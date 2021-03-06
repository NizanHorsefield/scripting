import sys
import getopt
import string

bpmEnabled  = <%= @bpm_enabled %>

def printUsage():
        print ' '
        print 'Usage'
        print '-----'
        print ' '
        print '<JAVA_HOME>/bin/java weblogic.WLST <ORACLE_HOME>/bin/soa-createUDD.py  --domain_home <doamin_home_dir> --soacluster <soa_cluster_name> --bamcluster <bam_cluster_name> --extend <true|false>'
        print ' '

def getCurrentUMSServerCnt():
        s = ls('/JMSServer')
        count = s.count("UMSJMSServer_auto")
        return count + 1

def createFileStore(storeName, serverName):
    create(storeName, 'FileStore')
    cd('/FileStore/'+storeName)
    set ('Target', serverName)
    set ('Directory', storeName)
    cd('/')

def createJDBCStore(storeName, prefixName, serverName):
    create(storeName, 'JDBCStore')
    cd('/JDBCStore/'+storeName)
    set ('DataSource', 'JMSDataSource')
    set ('PrefixName', prefixName)
    set ('Target', serverName)
    cd('/')

def createJMSServers(cluster, track, currentServerCnt, prefix):
        print ' '
        print "Creating JMS Servers for the cluster :- ", cluster
        s = ls('/Server')
        print ' '
        clustername = " "
        serverCnt = currentServerCnt
        tokens = s.split("drw-")
        tokens.sort()
        for token in tokens:
                token=token.strip().lstrip().rstrip()
                path="/Server/"+token
                cd(path)
                if not token == 'AdminServer' and not token == '':
                        clustername = get('Cluster')
                        print "Cluster Associated with the Server [",token,"] :- ",clustername
                        print ' '
                        searchClusterStr = cluster+":"
                        clusterNameStr = str(clustername)
                        print "searchClusterStr = ",searchClusterStr
                        print "clusterNameStr = ",clusterNameStr
                        if not clusterNameStr.find(searchClusterStr) == -1:
                                print token, " is associated with ", cluster
                                print ' '
                                print "Creating JMS Servers for ", track
                                print ' '
                                cd('/')

                                if track == 'soa':
                                        jmsServerName = 'SOAJMSServer_auto_'+str(serverCnt)
                                        #fileStoreName = 'SOAJMSServerFileStore_auto_'+str(serverCnt)
                                        jdbcStoreName = 'SOAJMSServerJDBCStore_auto_'+str(serverCnt)
                                        jdbcStorePrefix = prefix+str(serverCnt)
                                elif track == 'bam':
                                        jmsServerName = 'BAMJMSServer_auto_'+str(serverCnt)
                                        #fileStoreName = 'BAMJMSServerFileStore_auto_'+str(serverCnt)
                                        jdbcStoreName = 'BAMJMSServerJDBCStore_auto_'+str(serverCnt)
                                        jdbcStorePrefix = prefix+str(serverCnt)
                                elif track == 'ums':
                                        jmsServerName = 'UMSJMSServer_auto_'+str(serverCnt)
                                        #fileStoreName = 'UMSJMSServerFileStore_auto_'+str(serverCnt)
                                        jdbcStoreName = 'UMSJMSServerJDBCStore_auto_'+str(serverCnt)
                                        jdbcStorePrefix = prefix+str(serverCnt)

                                #createFileStore(fileStoreName, token)
                                #print "Created File Store :- ", fileStoreName

                                createJDBCStore(jdbcStoreName, jdbcStorePrefix, token)
                                print "Created JDBC Store :- ", jdbcStoreName

                                create(jmsServerName, 'JMSServer')
                                print "Created JMS Server :- ", jmsServerName
                                print ' '
                                assign('JMSServer', jmsServerName, 'Target', token)
                                print jmsServerName, " assigned to server :- ", token
                                print ' '
                                cd('/JMSServer/'+jmsServerName)
                                #set ('PersistentStore', fileStoreName)
                                set ('PersistentStore', jdbcStoreName)
                                
                                serverCnt = serverCnt + 1

def getClusterName(targetServer):
        targetServerStr = str(targetServer)
        s = ls('/Server')
        print ' '
        clustername = " "
        tokens = s.split("drw-")
        tokens.sort()
        for token in tokens:
                token=token.strip().lstrip().rstrip()
                path="/Server/"+token
                cd(path)
                if not token == 'AdminServer' and not token == '':
                        if not targetServerStr.find(token+":") == -1:
                                clustername = get('Cluster')
        return clustername

def getUMSJMSServers(cluster):
        s = ls('/JMSServers')
        jmsServersStr = " "
        print ' '
        clustername = " "
        tokens = s.split("drw-")
        tokens.sort()
        for token in tokens:
                token=token.strip().lstrip().rstrip()
                if not token == '' and not token.find("UMSJMSServer_auto") == -1:
                        cd('/JMSServers/'+token)
                        targetServer = get('Target')
                        clustername = getClusterName(targetServer)
                        searchClusterStr = cluster+":"
                        clusterNameStr = str(clustername)
                        print "searchClusterStr = ",searchClusterStr
                        print "clusterNameStr = ",clusterNameStr
                        if not clusterNameStr.find(searchClusterStr) == -1:
                                jmsServersStr = jmsServersStr + token + ","
        print "UMS JMS Servers for Cluster :- ", cluster , " is :- ", jmsServersStr
        return jmsServersStr


domain_home=soacluster=bamcluster=create_jms=" "
extend="false"

try:
        options,remainder = getopt.getopt(sys.argv[1:],'', ['soacluster=', 'bamcluster=', 'domain_home=', 'create_jms=','extend='])
except getopt.error, msg:
        printUsage()
        sys.exit()

for opt, arg in options:
    if opt == '--soacluster':
        soacluster = arg
    elif opt == '--bamcluster':
        bamcluster = arg
    elif opt == '--domain_home':
        domain_home= arg
    elif opt == '--create_jms':
        create_jms = arg
    elif opt == '--extend':
        extend = arg

if domain_home.isspace():
   printUsage()
   sys.exit()

if soacluster.isspace() and bamcluster.isspace():
   printUsage()
   sys.exit()

if not extend.isspace():
   if not extend == 'true' and not extend == 'false':
        printUsage()
        sys.exit()


if not soacluster.isspace() and not bamcluster.isspace():
        track="soa+bam"
elif soacluster.isspace() and not bamcluster.isspace():
        track="bam"
elif bamcluster.isspace() and not soacluster.isspace():
        track="soa"

print ' '
print 'Domain Home: ',domain_home
print 'SOA Cluster  : ', soacluster
print 'BAM Cluster  : ',bamcluster
print 'Track : ', track
print ' '

readDomain(domain_home)

if track == 'soa' or track == 'soa+bam':
        if not create_jms == 'true':
                print ("***Deleting SOA JMS Module ***");
                cd('/')
                try:
                        delete('SOAJMSModule','JMSSystemResource')
                except:
                  pass

        if create_jms == 'true':
                print ' '
                print "Creating the SOA JMS Servers for the cluster :- ", soacluster
                if bpmEnabled == true:
                  createJMSServers(soacluster, 'soa', 1, 'SOAJMSBPM_')
                else:
                  createJMSServers(soacluster, 'soa', 1, 'SOAJMS_')

        print ' '
        print '***Creating Uniform Distributed Destination for SOA***'
        cd('/')
        create('SOAJMSModuleUDDs','JMSSystemResource')

        print ' '
        print ("*** Setting Target for JMS Module***")
        cd('/')
        cd('JMSSystemResource/SOAJMSModuleUDDs')
        assign('JMSSystemResource', 'SOAJMSModuleUDDs', 'Target', soacluster)

        print ("*** Creating JMS SubModule for SOA JMS Servers***")
        cd('/')
        cd('JMSSystemResource/SOAJMSModuleUDDs')
        create('SOAJMSSubDM', 'SubDeployment')

        cd('/')
        cd('JMSSystemResource/SOAJMSModuleUDDs/SubDeployments/SOAJMSSubDM')

        print ' '
        print ("*** Listing SOA JMS Servers ***")
        s = ls('/JMSServers')
        soaJMSServerStr=''
        tokens = s.split("drw-")
        tokens.sort()
        for token in tokens:
                token=token.strip().lstrip().rstrip()
                if not token.find("SOAJMSServer_auto") == -1:
                        soaJMSServerStr = soaJMSServerStr + token +","
                print token

        soaJMSSrvCnt=string.count(s, 'SOAJMSServer_auto')
        print ' '
        print "Number of SOA JMS Servers := ", soaJMSSrvCnt
        print ' '
        print "soaJMSServerStr := ", soaJMSServerStr
        print ' '

        print ("*** Setting JMS SubModule for SOA JMS Server's target***")
        assign('JMSSystemResource.SubDeployment', 'SOAJMSModuleUDDs.SOAJMSSubDM', 'Target', soaJMSServerStr)

        cd('/')
        cd('JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0')
        print ("*** Creating Queues for SOA***")

        udd=create('TestFwkQueue','UniformDistributedQueue')
        udd.setJNDIName('jms/testfwk/TestFwkQueue')
        udd.setSubDeploymentName('SOAJMSSubDM')

        udd=create('B2BEventQueue','UniformDistributedQueue')
        udd.setJNDIName('jms/b2b/B2BEventQueue')
        udd.setSubDeploymentName('SOAJMSSubDM')
        udd.setJMSCreateDestinationIdentifier('jms/b2b/B2BEventQueue')

        udd=create('NotificationSenderQueue','UniformDistributedQueue')
        udd.setJNDIName('jms/Queue/NotificationSenderQueue')
        udd.setSubDeploymentName('SOAJMSSubDM')

        udd=create('B2B_IN_QUEUE','UniformDistributedQueue')
        udd.setJNDIName('jms/b2b/B2B_IN_QUEUE')
        udd.setSubDeploymentName('SOAJMSSubDM')
        udd.setJMSCreateDestinationIdentifier('jms/b2b/B2B_IN_QUEUE')

        udd=create('B2B_OUT_QUEUE','UniformDistributedQueue')
        udd.setJNDIName('jms/b2b/B2B_OUT_QUEUE')
        udd.setSubDeploymentName('SOAJMSSubDM')
        udd.setJMSCreateDestinationIdentifier('jms/b2b/B2B_OUT_QUEUE')

        #Bug Fix 8847268
        udd=create('EDNQueue','UniformDistributedQueue')
        udd.setJNDIName('jms/fabric/EDNQueue')
        udd.setSubDeploymentName('SOAJMSSubDM')


        print ("*** Creating Topics For SOA ***")
        udd=create('B2BBroadcastTopic','UniformDistributedTopic')
        udd.setJNDIName('jms/b2b/B2BBroadcastTopic')
        udd.setJMSCreateDestinationIdentifier('jms/b2b/B2BBroadcastTopic')
        udd.setSubDeploymentName('SOAJMSSubDM')

        #Bug Fix 8818202
        udd=create('XmlSchemaChangeNotificationTopic','UniformDistributedTopic')
        udd.setJNDIName('jms/fabric/XmlSchemaChangeNotificationTopic')
        udd.setJMSCreateDestinationIdentifier('jms/fabric/XmlSchemaChangeNotificationTopic')
        udd.setSubDeploymentName('SOAJMSSubDM')

        print ("*** Creating Connection Factories For SOA ***")

        soacf=create('TestFwkQueueFactory','ConnectionFactory')
        soacf.setJNDIName('jms/testfwk/TestFwkQueueFactory')
        #soacf.setSubDeploymentName('SOAJMSSubDM')



        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/TestFwkQueueFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)

        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0')
        soacf=create('NotificationSenderQueueConnectionFactory','ConnectionFactory')
        soacf.setJNDIName('jms/Queue/NotificationSenderQueueConnectionFactory')
        #soacf.setSubDeploymentName('SOAJMSSubDM')


        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/NotificationSenderQueueConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)


        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0')
        soacf=create('B2BBroadcastTopicConnectionFactory','ConnectionFactory')
        soacf.setJNDIName('jms/b2b/B2BBroadcastTopicConnectionFactory')
        #soacf.setSubDeploymentName('SOAJMSSubDM')
        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/B2BBroadcastTopicConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)


        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0')
        soacf=create('B2BEventQueueConnectionFactory','ConnectionFactory')
        soacf.setJNDIName('jms/b2b/B2BEventQueueConnectionFactory')
        #soacf.setSubDeploymentName('SOAJMSSubDM')
        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/B2BEventQueueConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)


        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0')
        soacf=create('B2BQueueConnectionFactory','ConnectionFactory')
        soacf.setJNDIName('jms/b2b/B2BQueueConnectionFactory')
        #soacf.setSubDeploymentName('SOAJMSSubDM')
        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/B2BQueueConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)


        #Bug Fix 8818202
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0')
        soacf=create('XmlSchemaChangeNotificationConnectionFactory','ConnectionFactory')
        soacf.setJNDIName('jms/fabric/XmlSchemaChangeNotificationConnectionFactory')
        #soacf.setSubDeploymentName('SOAJMSSubDM')
        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/XmlSchemaChangeNotificationConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)

        #Bug Fix 8847268
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0')
        soacf=create('EDNConnectionFactory','ConnectionFactory')
        soacf.setJNDIName('jms/fabric/EDNConnectionFactory')
        #soacf.setSubDeploymentName('SOAJMSSubDM')
        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/EDNConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)

        #Bug Fix 8847268
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0')
        soacf=create('XAEDNConnectionFactory','ConnectionFactory')
        soacf.setJNDIName('jms/fabric/xaEDNConnectionFactory')
        #soacf.setSubDeploymentName('SOAJMSSubDM')
        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/SOAJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/XAEDNConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)



if track == 'bam' or track == 'soa+bam':
        if not create_jms == 'true':
                print ("***Deleting BAM JMS Module ***");
                cd('/')
                try:
                        delete('BAMJmsSystemResource','JMSSystemResource')
                except:
                   pass

        if create_jms == 'true':
                print ' '
                print "Creating the BAM JMS Servers for the cluster :- ", bamcluster
                if bpmEnabled == true:
                  createJMSServers(bamcluster, 'bam', 1, 'BAMJMSBPM_')
                else:
                  createJMSServers(bamcluster, 'bam', 1, 'BAMJMS_')


        print ' '
        print '***Creating Uniform Distributed Destination for BAM***'
        cd('/')
        create('BAMJMSModuleUDDs','JMSSystemResource')

        print ("*** Setting Target for JMS Module***")
        cd('/')
        cd('JMSSystemResource/BAMJMSModuleUDDs')
        assign('JMSSystemResource', 'BAMJMSModuleUDDs', 'Target', bamcluster)

        print ("*** Creating JMS SubModule for BAM JMS Servers***")
        cd('/')
        cd('JMSSystemResource/BAMJMSModuleUDDs')
        create('BAMJMSSubDM', 'SubDeployment')

        cd('/')
        cd('JMSSystemResource/BAMJMSModuleUDDs/SubDeployments/BAMJMSSubDM')
        print ' '
        print ("*** Listing BAM JMS Servers ***")
        jmssrvlist = ls('/JMSServers')
        bamJMSServerStr=''
        for token in jmssrvlist.split("drw-"):
                token=token.strip().lstrip().rstrip()
                if not token.find("BAMJMSServer_auto") == -1:
                        bamJMSServerStr = bamJMSServerStr + token +","
                print token

        bamJMSSrvCnt=string.count(jmssrvlist, 'BAMJMSServer_auto')
        print ' '
        print "Number of BAM JMS Servers := ", bamJMSSrvCnt
        print ' '
        print "bamJMSServerStr := ", bamJMSServerStr
        print ' '

        print ("*** Setting JMS SubModule for BAM JMS Server's target***")
        assign('JMSSystemResource.SubDeployment', 'BAMJMSModuleUDDs.BAMJMSSubDM', 'Target', bamJMSServerStr)


        cd('/')
        cd('JMSSystemResource/BAMJMSModuleUDDs/JmsResource/NO_NAME_0')

        print ("*** Creating Queues for BAM ***")
        udd=create('demoQueue','UniformDistributedQueue')
        udd.setJNDIName('jms/demoQueue')
        udd.setSubDeploymentName('BAMJMSSubDM')

        print ("*** Creating Topics For BAM ***")
        udd=create('oracle.bam.messaging.activedatacache.activedata','UniformDistributedTopic')
        udd.setJNDIName('topic/oracle.bam.messaging.activedatacache.activedata')
        udd.setSubDeploymentName('BAMJMSSubDM')

        udd=create('oracle.bam.messaging.systemobjectnotification','UniformDistributedTopic')
        udd.setJNDIName('topic/oracle.bam.messaging.systemobjectnotification')
        udd.setSubDeploymentName('BAMJMSSubDM')

        udd=create('oracle.bam.messaging.reportcache.activedata','UniformDistributedTopic')
        udd.setJNDIName('topic/oracle.bam.messaging.reportcache.activedata')
        udd.setSubDeploymentName('BAMJMSSubDM')

        udd=create('oracle.bam.messaging.deliverystatusnotification','UniformDistributedTopic')
        udd.setJNDIName('topic/oracle.bam.messaging.deliverystatusnotification')
        udd.setSubDeploymentName('BAMJMSSubDM')

        udd=create('demoTopic','UniformDistributedTopic')
        udd.setJNDIName('jms/demoTopic')
        udd.setSubDeploymentName('BAMJMSSubDM')

        print ("*** Creating Connection Factories For BAM ***")
        bamcf=create('BAMJMSConnectionFactory','ConnectionFactory')
        bamcf.setJNDIName('jms/QueueConnectionFactory')
        #bamcf.setSubDeploymentName('BAMJMSSubDM')

        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/BAMJMSModuleUDDs/JmsResource/NO_NAME_0/ConnectionFactory/BAMJMSConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)

#UMS

print ' '
print ("***Removing existing UMS  Modules***")
cd('/')

if not create_jms == 'true':
        #delete('configwiz-jms','JMSSystemResource')
        if not extend == 'true':
                try:
                        delete('UMSJMSSystemResource','JMSSystemResource')
                except:
                   pass
if create_jms == 'true':
        if bpmEnabled == true:
          prefix = 'UMSJMSBPM_'
        else:
          prefix = 'UMSJMS_'
        print ' '
        if track == 'soa':
                createJMSServers(soacluster, 'ums', getCurrentUMSServerCnt(), prefix)
        elif track == 'bam':
                createJMSServers(bamcluster, 'ums',  getCurrentUMSServerCnt(), prefix)
        elif track == 'soa+bam':
                createJMSServers(soacluster, 'ums',  getCurrentUMSServerCnt(), prefix)
                createJMSServers(bamcluster, 'ums', getCurrentUMSServerCnt(), prefix)

if not track.find('soa') == -1:
        print ' '
        print ("*** Creating Uniform Distributed Destinations for UMS SOA ***")
        print ' '
        print ("*** Creating UMSJMSSystemResource for SOA ***")


        jmsSystemResourceNameSOA = ""
        if track == "soa":
                if extend == "true":
                        jmsSystemResourceNameSOA = "UMSJMSModuleUDDsSOA"
                else:
                        jmsSystemResourceNameSOA = "UMSJMSSystemResource"
        elif track == "soa+bam":
                jmsSystemResourceNameSOA = "UMSJMSModuleUDDsSOA"


        cd('/')
        create(jmsSystemResourceNameSOA,'JMSSystemResource')

        cd('/JMSSystemResource/'+jmsSystemResourceNameSOA)
        print ' '
        print "Targeting ",jmsSystemResourceNameSOA, " to SOA Cluster :- ", soacluster
        assign('JMSSystemResource', jmsSystemResourceNameSOA, 'Target', soacluster)


        print ("*** Creating JMS SubModule for UMS SOA JMS Servers***")
        cd('/')
        cd('JMSSystemResource/'+jmsSystemResourceNameSOA)
        create('UMSJMSSubDMSOA', 'SubDeployment')

        umsJMSServerStr = getUMSJMSServers(soacluster)
        print ' '

        print ("*** Setting JMS SubModule for UMS SOA JMS Server's target***")
        print "umsJMSServerStr = ",umsJMSServerStr
        umsJMSServerStr = umsJMSServerStr.strip().lstrip().rstrip()
        assign('JMSSystemResource.SubDeployment', jmsSystemResourceNameSOA+'.UMSJMSSubDMSOA', 'Target', umsJMSServerStr)

        print ("*** Creating Queues for UMS ***")
        cd('/')
        cd('JMSSystemResource/'+jmsSystemResourceNameSOA+'/JmsResource/NO_NAME_0')
        print ' '

        udd=create('OraSDPMEngineCmdQ','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineCmdQ')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMEngineSndQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMEngineRcvQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMDriverDefSndQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMDriverDefSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMAppDefRcvQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        udd=create('OraSDPMWSRcvQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMWSRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMSOA')

        print("*** Creating Connection Factories for UMS ***");

        cf1=create('OraSDPMQueueConnectionFactory','ConnectionFactory')
        cf1.setJNDIName('OraSDPM/QueueConnectionFactory')
        #cf1.setSubDeploymentName('UMSJMSSubDMSOA')

        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/'+jmsSystemResourceNameSOA+'/JmsResource/NO_NAME_0/ConnectionFactory/OraSDPMQueueConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)

if not track.find('bam') == -1:
        print ' '
        print ("*** Creating Uniform Distributed Destinations for UMS BAM  ***")
        print ' '
        print ("*** Creating UMSJMSSystemResource for BAM  ***")
        cd('/')

        jmsSystemResourceNameBAM = ""
        if track == "bam":
                if extend == "true":
                        jmsSystemResourceNameBAM = "UMSJMSModuleUDDsBAM"
                else:
                        jmsSystemResourceNameBAM = "UMSJMSSystemResource"
        elif track == "soa+bam":
                jmsSystemResourceNameBAM = "UMSJMSModuleUDDsBAM"


        create(jmsSystemResourceNameBAM,'JMSSystemResource')

        cd('/JMSSystemResource/'+jmsSystemResourceNameBAM)
        print ' '
        print "Targeting ",jmsSystemResourceNameBAM+" to BAM Cluster :- ", bamcluster
        assign('JMSSystemResource', jmsSystemResourceNameBAM, 'Target', bamcluster)

        print ("*** Creating JMS SubModule for UMS BAM JMS Servers***")
        cd('/')
        cd('JMSSystemResource/'+jmsSystemResourceNameBAM)
        create('UMSJMSSubDMBAM', 'SubDeployment')

        umsJMSServerStr = getUMSJMSServers(bamcluster)
        print ' '

        print ("*** Setting JMS SubModule for UMS BAM JMS Server's target***")
        umsJMSServerStr = umsJMSServerStr.strip().lstrip().rstrip()
        assign('JMSSystemResource.SubDeployment', jmsSystemResourceNameBAM+'.UMSJMSSubDMBAM', 'Target', umsJMSServerStr)

        print ("*** Creating Queues for UMS ***")
        cd('/')
        cd('JMSSystemResource/'+jmsSystemResourceNameBAM+'/JmsResource/NO_NAME_0')
        print ' '

        udd=create('OraSDPMEngineCmdQ','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineCmdQ')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMEngineSndQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMEngineRcvQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMEngineRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMDriverDefSndQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMDriverDefSndQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMAppDefRcvQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMAppDefRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        udd=create('OraSDPMWSRcvQ1','UniformDistributedQueue')
        udd.setJNDIName('OraSDPM/Queues/OraSDPMWSRcvQ1')
        udd.setSubDeploymentName('UMSJMSSubDMBAM')

        print("*** Creating Connection Factories for UMS ***");

        cf1=create('OraSDPMQueueConnectionFactory','ConnectionFactory')
        cf1.setJNDIName('OraSDPM/QueueConnectionFactory')
        #cf1.setSubDeploymentName('UMSJMSSubDMBAM')

        print ("*** Enabling XA ***")
        cd('/JMSSystemResource/'+jmsSystemResourceNameBAM+'/JmsResource/NO_NAME_0/ConnectionFactory/OraSDPMQueueConnectionFactory')
        set('DefaultTargetingEnabled', 'true')
        create('TransactionParams', 'TransactionParams')
        cd('TransactionParams/NO_NAME_0')
        cmo.setXAConnectionFactoryEnabled(true)
print ' '
print ("*** Saving the domain ***")


updateDomain()

#dumpStack()