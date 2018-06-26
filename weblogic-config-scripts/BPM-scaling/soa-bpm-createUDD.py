#==========================================================================
# FileName      : wlst/BPM-scaling/soa-bpm-createUDD.py
# Updated       : 23/05/2017
# Author        : Nizan Horsefield
# Description:
# This script will create Distributed JMS objects required by BPM
#==========================================================================

import sys
import getopt
import string

#WLHOME='/opt/nextees/middleware/wlserver_10.3'
WLHOME='/home/oracle/Oracle/Middleware/wlserver_10.3/'
#DOMAIN_PATH='/opt/nextees/middleware/user_projects/domains/soaosb_domain_test'
DOMAIN_PATH='/home/oracle/Oracle/Middleware/user_projects/domains/soa_singleton_domain/'

soacluster  = 'soa_cluster'
Admin       = 'AdminServer'

bpmEnabled  = true
ofm_version = 1117

def deleteFileStores():
    filestores = ls('/FileStore/')
    print ' '
    fs = filestores.split("drw-")
    fs.sort()
    for f in fs:
        f=f.strip().lstrip().rstrip()
        print f
        delete(f,'FileStore')

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

def createjmsservers(cluster, track, currentServerCnt, prefix):
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

                if track == 'bpm':
                    jmsServerName = 'BPMJMSServer_auto_'+str(serverCnt)
                    fileStoreName = 'BPMJMSServerFileStore_auto_'+str(serverCnt)
                    #jdbcStoreName = 'BPMJMSServerJDBCStore_auto_'+str(serverCnt)
                    #jdbcStorePrefix = prefix+str(serverCnt)
                elif track == 'ag':
                    jmsServerName = 'AGJMSServer_auto_'+str(serverCnt)
                    fileStoreName = 'AGJMSServerFileStore_auto_'+str(serverCnt)
                    #jdbcStoreName = 'AGJMSServerJDBCStore_auto_'+str(serverCnt)
                    #jdbcStorePrefix = prefix+str(serverCnt)
                elif track == 'ps6soa' and ofm_version > 1116:
                    jmsServerName = 'PS6SOAJMSServer_auto_'+str(serverCnt)
                    fileStoreName = 'PS6SOAJMSServerFileStore_auto_'+str(serverCnt)
                    #jdbcStoreName = 'PS6SOAJMSServerJDBCStore_auto_'+str(serverCnt)
                    #jdbcStorePrefix = prefix+str(serverCnt)
                elif track == 'soa' and ofm_version > 1116:
                    jmsServerName = 'SOAJMSServer_auto_'+str(serverCnt)
                    fileStoreName = 'SOAJMSServerFileStore_auto_'+str(serverCnt)
                    #jdbcStoreName = 'SOAJMSServerJDBCStore_auto_'+str(serverCnt)
                    #jdbcStorePrefix = prefix+str(serverCnt)
                elif track == 'ums' and ofm_version > 1116:
                    jmsServerName = 'UMSJMSServer_auto_'+str(serverCnt)
                    fileStoreName = 'UMSJMSServerFileStore_auto_'+str(serverCnt)
                    #jdbcStoreName = 'UMSSOAJMSServerJDBCStore_auto_'+str(serverCnt)
                    #jdbcStorePrefix = prefix+str(serverCnt)
                        
                createFileStore(fileStoreName, token)
                print "Created File Store :- ", fileStoreName
                
                #createJDBCStore(jdbcStoreName, jdbcStorePrefix, token)
                #print "Created JDBC Store :- ", jdbcStoreName

                create(jmsServerName, 'JMSServer')
                print "Created JMS Server :- ", jmsServerName
                print ' '
                assign('JMSServer', jmsServerName, 'Target', token)
                print jmsServerName, " assigned to server :- ", token 
                print ' '
                cd('/JMSServer/'+jmsServerName)
                set ('PersistentStore', fileStoreName)
                #set ('PersistentStore', jdbcStoreName)

                serverCnt = serverCnt + 1

def createudd(module,queue,subd,jndi_prefix):
    print 'Creating '+queue+' in '+module+ ' and setting '+subd
    cd('/JMSSystemResource/'+module+'/JmsResource/NO_NAME_0')
    udd=create(queue,'UniformDistributedQueue')
    udd.setJNDIName(jndi_prefix+'/'+queue)
    udd.setJMSCreateDestinationIdentifier('jms/bpm/'+queue)
    udd.setSubDeploymentName(subd)

def createquota(module,quota,subd,jndi_prefix):
    print 'Creating '+quota+' in '+module+ ' and setting '+subd
    cd('/JMSSystemResource/'+module+'/JmsResource/NO_NAME_0')
    udd=create(quota,'Quota')
    udd.setJNDIName(jndi_prefix+'/'+quota)
    udd.setJMSCreateDestinationIdentifier('jms/bpm/'+quota)
    udd.setSubDeploymentName(subd)

def createtopic(module,topic,subd,jndi_prefix):
    print 'Creating '+topic+' in '+module+ ' and setting '+subd
    cd('/JMSSystemResource/'+module+'/JmsResource/NO_NAME_0')
    udd=create(topic,'UniformDistributedTopic')
    udd.setJNDIName(jndi_prefix+'/'+topic)
    udd.setJMSCreateDestinationIdentifier('jms/bpm/'+topic)
    udd.setSubDeploymentName(subd)

def createcf(module,cf,jndi_prefix):
    print 'Creating '+cf+' in '+module
    cd('/JMSSystemResource/'+module+'/JmsResource/NO_NAME_0')
    soacf=create(cf,'ConnectionFactory')
    soacf.setJNDIName(jndi_prefix+'/'+cf)
    cd('/JMSSystemResource/'+module+'/JmsResource/NO_NAME_0/ConnectionFactory/'+cf)
    set('DefaultTargetingEnabled', 'true')
    create('TransactionParams', 'TransactionParams')
    cd('TransactionParams/NO_NAME_0')
    cmo.setXAConnectionFactoryEnabled(true)

def createmodulesubd(module,subd,prefix):

    print ("*** Listing "+prefix+" JMS Servers ***")
    s = ls('/JMSServers')
    soaJMSServerStr=''
    tokens = s.split("drw-")
    tokens.sort()
    for token in tokens:
        token=token.strip().lstrip().rstrip()
        if not token.find(prefix) == -1:
            soaJMSServerStr = soaJMSServerStr + token +","
        print token

    soaJMSSrvCnt=string.count(s, prefix)
    print ' '
    print "Number of "+prefix+" JMS Servers := ", soaJMSSrvCnt
    print ' '
    print "soaJMSServerStr := ", soaJMSServerStr
    print ' '

    print 'Creating '+module+' and '+subd+' targeting '+soaJMSServerStr
    cd('/')
    create(module,'JMSSystemResource')
    cd('/JMSSystemResource/'+module)
    assign('JMSSystemResource', module, 'Target', soacluster)
    cd('/JMSSystemResource/'+module)
    create(subd, 'SubDeployment')
    cd('/JMSSystemResource/'+module+'/SubDeployments/'+subd)
    print ("*** Setting JMS SubModule for SOA JMS Server's target***")
    assign('JMSSystemResource.SubDeployment', module+'.'+subd, 'Target', soaJMSServerStr)

def configureagjms():
    prefix = 'AGJMSServer_auto'
    module = 'AGJMSModuleUDDs'
    subd = 'AGJMSSubDM'
    topics = 'UIBrokerTopic'
    cfs = 'UIBrokerTopicConnectionFactory'
    jndi_prefix = 'jms/bpm'

    if bpmEnabled == true:
        createjmsservers(soacluster, 'ag', 1, 'AGJMSBPM_')
        # create the Distributed JMS Module AGJMSModuleUDDs and Subdeployment
        createmodulesubd(module,subd,prefix)

        # create the JMS resources and assign to the AGJMSSubDM
        ## Queues
        for t in topics.split(','):
            createtopic(module,t,subd,jndi_prefix)
            ##connectionfactories
        for cf in cfs.split(','):
            createcf(module,cf,jndi_prefix)
            # AG jms end

def configurebpmjms():
    prefix = 'BPMJMSServer_auto'
    module = 'BPMJMSModuleUDDs'
    subd = 'BPMJMSSubDM'
    topics = 'MeasurementTopic,PeopleQueryTopic'
    cfs = 'BAMCommandXAConnectionFactory,CubeCommandXAConnectionFactory,MeasurementTopicConnectionFactory,PeopleQueryConnectionFactory,PeopleQueryTopicConnectionFactory'
    jndi_prefix = 'jms/bpm'

    if bpmEnabled == true:
        try:
            createjmsservers(soacluster, 'bpm', 1, 'BPMJMSBPM_')
        except:
            print 'JMSServer creation failed for BPMJMSBPM_'
    else:
        try:
            createjmsservers(soacluster, 'bpm', 1, 'BPMJMS_')
        except:
            print 'JMSServer creation failed for BPMJMS_'

    # create the Distributed JMS Module BPMJMSModuleUDDs and Subdeployment
    createmodulesubd(module,subd,prefix)

    # create the JMS resources and assign to the BPMJMSSubD
    ## Queues
    for t in topics.split(','):
        createtopic(module,t,subd,jndi_prefix)
    ##connectionfactories
    for cf in cfs.split(','):
        createcf(module,cf,jndi_prefix)
    # bpm jms end

def configureps6jms():
    prefix = 'PS6SOAJMSServer_auto'
    module = 'PS6SOAJMSModuleUDDs'
    subd = 'PS6SOAJMSSubDM'
    cfs = 'CaseEventConnectionFactory'
    udds = 'CaseEventQueue'
    jndi_prefix = 'jms/bpm'

    if ofm_version > 1116:
        if bpmEnabled == true:
          createjmsservers(soacluster, 'ps6soa', 1, 'PS6SOAJMSBPM_')
        else:
          createjmsservers(soacluster, 'ps6soa', 1, 'PS6SOA_')
        # create the Distributed JMS Module PS6SOAJMSModuleUDDs and Subdeployment
        createmodulesubd(module,subd,prefix)
    else:
        print "Warning: PS6 components not created. This is expected behaviour for versions of OFM 11.1.1.6 and below."

    print ("*** Setting JMS SubModule for PS6 JMS Server's target***")
    if ofm_version > 1116:
        # create the JMS resources and assign to the PS6SOAJMSSubDM
        ## Queues
        for u in udds.split(','):
            createudd(module,u,subd,jndi_prefix)
            ##connectionfactories
        for cf in cfs.split(','):
            createcf(module,cf,jndi_prefix)
            # PS6 jms end
    else:
        print "Warning: PS6 components not created. This is expected behaviour for versions of OFM 11.1.1.6 and below."

def configuresoajms():
    prefix = 'SOAJMSServer_auto'
    module = 'SOAJMSModuleUDDs'
    subd = 'SOAJMSSubDM'

    topics1 = 'B2BBroadcastTopic'
    cfs1 = 'B2BBroadcastTopicConnectionFactory,B2BEventQueueConnectionFactory,B2BQueueConnectionFactory'
    udds1 = 'B2BEventQueue,B2B_IN_QUEUE,B2B_OUT_QUEUE'
    jndi_prefix1 = 'jms/b2b'

    cfs2 = 'EDNConnectionFactory,XAEDNConnectionFactory,XmlSchemaChangeNotificationConnectionFactory'
    udds2 = 'EDNQueue'
    topics2 = 'XmlSchemaChangeNotificationTopic'
    jndi_prefix2 = 'jms/fabric'

    cfs3 = 'NotificationSenderQueueConnectionFactory'
    udds3 = 'NotificationSenderQueue'
    jndi_prefix3 = 'jms/Queue'

    cfs4 = 'TestFwkQueueFactory'
    udds4 = 'TestFwkQueue'
    jndi_prefix4 = 'jms/testfwk'


    cd('/')
    if ofm_version > 1116:
        dumpStack()
        if bpmEnabled == true:
            createjmsservers(soacluster, 'soa', 1, 'SOAJMSBPM_')
        else:
            createjmsservers(soacluster, 'soa', 1, 'SOA_')
        # create the Distributed JMS Module SOAJMSModuleUDDs and Subdeployment
        createmodulesubd(module,subd,prefix)
    else:
        print "Warning: SOA components not created. This is expected behaviour for versions of OFM 11.1.1.6 and below."

    if ofm_version > 1116:
        # create the JMS resources and assign to the SOAJMSSubDM
        ## Queues
        for u in udds1.split(','):
            createudd(module,u,subd,jndi_prefix1)
        ## Topics
        for t in topics1.split(','):
            createtopic(module,t,subd,jndi_prefix1)
            ##connectionfactories
        for cf in cfs1.split(','):
            createcf(module,cf,jndi_prefix1)

        ## Queues
        for u in udds2.split(','):
            createudd(module,u,subd,jndi_prefix2)
        ## Topics
        for t in topics2.split(','):
            createtopic(module,t,subd,jndi_prefix2)
            ##connectionfactories
        for cf in cfs2.split(','):
            createcf(module,cf,jndi_prefix2)

        ## Queues
        for u in udds3.split(','):
            createudd(module,u,subd,jndi_prefix3)
            ##connectionfactories
        for cf in cfs3.split(','):
            createcf(module,cf,jndi_prefix3)

        ## Queues
        for u in udds4.split(','):
            createudd(module,u,subd,jndi_prefix4)
            ##connectionfactories
        for cf in cfs4.split(','):
            createcf(module,cf,jndi_prefix4)
            # SOA jms end
    else:
        print "Warning: SOA components not created. This is expected behaviour for versions of OFM 11.1.1.6 and below."

def configureumsjms():
    prefix = 'UMSJMSServer_auto'
    module = 'UMSJMSModuleUDDs'
    subd = 'UMSJMSSubDM'
    udds = 'OraSDPMAppDefRcvQ1,OraSDPMDriverDefSndQ1,OraSDPMEngineCmdQ,OraSDPMEngineRcvQ1,OraSDPMEngineSndQ1,OraSDPMWSRcvQ1'
    cfs = 'OraSDPMQueueConnectionFactory'
    jndi_prefix = 'OraSDPM/Queues'

    if ofm_version > 1116:
        dumpStack()
        if bpmEnabled == true:
            createjmsservers(soacluster, 'ums', 1, 'UMSJMSBPM_')
        else:
            createjmsservers(soacluster, 'ums', 1, 'UMS_')
        # create the Distributed JMS Module UMSJMSModuleUDDs and Subdeployment
        createmodulesubd(module,subd,prefix)
    else:
        print "Warning: UMS components not created. This is expected behaviour for versions of OFM 11.1.1.6 and below."

    if ofm_version > 1116:
        # create the JMS resources and assign to the UMSJMSSubDM
        ## Queues
        for u in udds.split(','):
            createudd(module,u,subd,jndi_prefix)
            ##connectionfactories
        for cf in cfs.split(','):
            createcf(module,cf,'OraSDPM')
            # UMS jms end
    else:
        print "Warning: UMS components not created. This is expected behaviour for versions of OFM 11.1.1.6 and below."

def main():
    print "The following WL Domain will be updated " +DOMAIN_PATH
    HitKey=raw_input('Press any key to continue...')
    # read in the current domain directory
    try:
        readDomain(DOMAIN_PATH)
        print 'Successfully read the BPM Domain.'
    except Exception, e:
        print 'Could not read the domain'
        print e
    # work
    print "Going to create the AG JMS objects"
    configureagjms()
    print "Done"

    print "Going to create the BPM JMS objects"
    configurebpmjms()
    print "Done"

    print "Going to create the SOA JMS objects"
    configuresoajms()
    print "Done"

    print "Going to create the PS6 JMS objects"
    configureps6jms()
    print "Done"

    print "Going to create the UMS JMS objects"
    configureumsjms()
    print "Done"

    print "Ready to update the domain"
    HitKey=raw_input('Press any key to continue...')
    try:
        updateDomain()
        print 'Successfully Updated SOA Domain.'
    except Exception, e:
        print 'Could not update the domain'
        print e
    print "Ready to close the domain"
    try:
        closeDomain()
        print 'Successfully closed the BPM Domain.'
    except Exception, e:
        print 'Could not close the domain'
        print e

main()