#==========================================================================
# FileName      : wlst/BPM-scaling/destroyJMSResources.py
# Updated       : 23/05/2017
# Author        : Nizan Horsefield
# Description:
# This script will destroy the JMS objects required by BPM
#==========================================================================

import sys
print "@@@ Starting the script ..."
from java.util import *
from javax.management import *

def connect2admin():
    adminURL='t3://192.168.33.56:7001'
    adminUserName='weblogic'
    adminPassword='password123'
    connect(adminUserName, adminPassword, adminURL)


    # the working functions
# delete UniformDistributedTopics
def deletedistributedtopic(module,topic):
    print "Deleting "+topic+ " from "+module
    try:
        cd('/JMSSystemResources/'+module+'/JMSResource/'+module)
        cmo.destroyUniformDistributedTopic(getMBean('/JMSSystemResources/'+module+'/JMSResource/'+module+'/UniformDistributedTopics/' +topic))
    except Exception, e:
        print 'Cannot deletev' +topic
        print e

#delete Topics
def deletetopic(module,topic):
    print "Deleting "+topic+ " from "+module
    try:
        cd('/JMSSystemResources/'+module+'/JMSResource/'+module)
        cmo.destroyUniformDistributedTopic(getMBean('/JMSSystemResources/'+module+'/JMSResource/'+module+'/Topics/' +topic))
    except Exception, e:
        print 'Cannot delete' +topic
        print e

# delete connection factory
def deletecf(module,cf):
    print "Deleting "+cf+ " from "+module
    try:
        cd('/JMSSystemResources/'+module+'/JMSResource/'+module)
        cmo.destroyConnectionFactory(getMBean('/JMSSystemResources/'+module+'/JMSResource/'+module+'/ConnectionFactories/'+cf))
    except Exception, e:
        print 'Cannot delete' +cf
        print e

# delete distributed queues
def deletequeue(module,queue):
    print "Deleting "+queue+ " from "+module
    try:
        cd('/JMSSystemResources/'+module+'/JMSResource/'+module)
        cmo.destroyUniformDistributedQueue(getMBean('/JMSSystemResources/'+module+'/JMSResource/'+module+'/UniformDistributedQueues/'+queue))
    except Exception, e:
        print 'Cannot delete' +queue
        print e

# delete JMS Quota
def deletequota(module,quota):
    print "Deleting "+quota+ " from "+module
    try:
        cd('/JMSSystemResources/'+module+'/JMSResource/'+module+'')
        cmo.destroyQuota(getMBean('/JMSSystemResources/'+module+'/JMSResource/'+module+'/Quotas/'+quota))
    except Exception, e:
        print 'Cannot delete' +quota
        print e

# delete the JMS Subdeployments
def deletejmssubdeployments(module,subdeployment):
    print "Deleting "+subdeployment+ " from "+module
    try:
        cd('/SystemResources/'+module)
        cmo.destroySubDeployment(getMBean('/SystemResources/'+module+'/SubDeployments/'+subdeployment))
    except Exception, e:
        print 'Cannot delete' +subdeployment
        print e

# delete the JMS Modules
def deletejsmmodules(module):
    print "Deleting "+module
    try:
        cd('/')
        cmo.destroyJMSSystemResource(getMBean('/SystemResources/'+module))
    except Exception, e:
        print 'Cannot delete' +module
        print e

# delete the JMS Servers
def deletejmsservers(servername):
    print "Deleting "+servername
    try:
        cmo.destroyJMSServer(getMBean('/Deployments/'+servername))
    except Exception, e:
        print 'Cannot delete' +servername
        print e

# delete the JMS Pstores
def deletejmspstores(storename):
    print "Deleting "+storename
    try:
        cmo.destroyFileStore(getMBean('/FileStores/'+storename))
    except Exception, e:
        print 'Cannot delete' +storename
        print e

# delete the JMS resources
def deleteagjmsresources():
    # delete AG JMS Resources
    module = 'AGJMSModuleUDDs'
    subd = 'AGJMSSubDM'
    jmsservers = 'AGJMSServer_auto_1,AGJMSServer_auto_2,AGJMSServer_auto_3,AGJMSServer_auto_4'
    pstores = 'AGJMSServerFileStore_auto_1,AGJMSServerFileStore_auto_2,AGJMSServerFileStore_auto_3,AGJMSServerFileStore_auto_4'
    topics = 'UIBrokerTopic'
    cfs = 'UIBrokerTopicConnectionFactory'

    # delete topics
    for t in topics.split(','):
        deletedistributedtopic(module,t)

    # delete connectionfactories
    for cf in cfs.split(','):
        deletecf(module,cf)

    # delete subdeployment
    for s in subd.split(','):
        deletejmssubdeployments(module,s)

    # delete module
    deletejsmmodules(module)

    # delete JMS servers
    for s in jmsservers.split(','):
        deletejmsservers(s)

    # delete JMS Pstores
    for p in pstores.split(','):
        deletejmspstores(p)

def deletebpmjmsresources():
    # delete BPM JMS Resources
    module = 'BPMJMSModuleUDDs'
    subd = 'BPMJMSSubDM'
    jmsservers = 'BPMJMSServer_auto_1,BPMJMSServer_auto_2,BPMJMSServer_auto_3,BPMJMSServer_auto_4'
    pstores = 'BPMJMSServerFileStore_auto_1,BPMJMSServerFileStore_auto_2,BPMJMSServerFileStore_auto_3,BPMJMSServerFileStore_auto_4'
    topics = 'MeasurementTopic,PeopleQueryTopic'
    cfs = 'BAMCommandXAConnectionFactory,CubeCommandXAConnectionFactory,MeasurementTopicConnectionFactory,PeopleQueryConnectionFactory,PeopleQueryTopicConnectionFactory'
    quotas = 'MeasurementQuota'

    # delete topics
    for t in topics.split(','):
        deletedistributedtopic(module,t)

    # delete connectionfactories
    for cf in cfs.split(','):
        deletecf(module,cf)

    # delete subdeployment
    deletejmssubdeployments(module,subd)

    # delete module
    deletejsmmodules(module)

    # delete JMS servers
    for s in jmsservers.split(','):
        deletejmsservers(s)

    # delete JMS Pstores
    for p in pstores.split(','):
        deletejmspstores(p)

def deleteps6jmsresources():
    # delete PS6 Resources
    module = 'PS6SOAJMSModuleUDDs'
    subd = 'PS6SOAJMSSubDM'
    jmsservers = 'PS6SOAJMSServer_auto_1,PS6SOAJMSServer_auto_2,PS6SOAJMSServer_auto_3,PS6SOAJMSServer_auto_4'
    pstores = 'PS6SOAJMSServerFileStore_auto_1,PS6SOAJMSServerFileStore_auto_2,PS6SOAJMSServerFileStore_auto_3,PS6SOAJMSServerFileStore_auto_4'
    cfs = 'CaseEventConnectionFactory'
    queues = 'CaseEventQueue'

    # delete connectionfactories
    for cf in cfs.split(','):
        deletecf(module,cf)

    # delete queues
    for q in queues.split(','):
        deletequeue(module,q)

    # delete subdeployment
    deletejmssubdeployments(module,subd)

    # delete module
    deletejsmmodules(module)

    # delete JMS servers
    for s in jmsservers.split(','):
        deletejmsservers(s)

    # delete JMS Pstores
    for p in pstores.split(','):
        deletejmspstores(p)

def deletesoajmsresources():
    # delete SOA Resources
    module = 'SOAJMSModuleUDDs'
    subd = 'SOAJMSSubDM'
    jmsservers = 'SOAJMSServer_auto_1,SOAJMSServer_auto_2,SOAJMSServer_auto_3,SOAJMSServer_auto_4'
    pstores = 'SOAJMSServerFileStore_auto_1,SOAJMSServerFileStore_auto_2,SOAJMSServerFileStore_auto_3,SOAJMSServerFileStore_auto_4'
    topics = 'B2BBroadcastTopic,XmlSchemaChangeNotificationTopic'
    cfs = 'B2BBroadcastTopicConnectionFactory,B2BEventQueueConnectionFactory,B2BQueueConnectionFactory,EDNConnectionFactory,NotificationSenderQueueConnectionFactory,TestFwkQueueFactory,XAEDNConnectionFactory,XmlSchemaChangeNotificationConnectionFactory'
    queues = 'B2BEventQueue,B2B_IN_QUEUE,B2B_OUT_QUEUE,EDNQueue,NotificationSenderQueue,TestFwkQueue'

    # delete topics
    for t in topics.split(','):
        deletedistributedtopic(module,t)

    # delete connectionfactories
    for cf in cfs.split(','):
        deletecf(module,cf)

    # delete queues
    for q in queues.split(','):
        deletequeue(module,q)

    # delete subdeployment
    deletejmssubdeployments(module,subd)

    # delete module
    deletejsmmodules(module)

    # delete JMS servers
    for s in jmsservers.split(','):
        deletejmsservers(s)

    # delete JMS Pstores
    for p in pstores.split(','):
        deletejmspstores(p)

def deleteumsjmsresources():
    # delete UMS resources
    module = 'UMSJMSModuleUDDs'
    subd = 'UMSJMSSubDM'
    jmsservers = 'UMSJMSServer_auto_1,UMSJMSServer_auto_2,UMSJMSServer_auto_3,UMSJMSServer_auto_4'
    pstores = 'UMSJMSServerFileStore_auto_1,UMSJMSServerFileStore_auto_2,UMSJMSServerFileStore_auto_3,UMSJMSServerFileStore_auto_4'
    cfs = 'OraSDPMQueueConnectionFactory'
    queues = 'OraSDPMAppDefRcvQ1,OraSDPMDriverDefSndQ1,OraSDPMEngineCmdQ,OraSDPMEngineRcvQ1,OraSDPMEngineSndQ1,OraSDPMWSRcvQ1'

    # delete connectionfactories
    for cf in cfs.split(','):
        deletecf(module,cf)

    # delete queues
    for q in queues.split(','):
        deletequeue(module,q)

    # delete subdeployment
    deletejmssubdeployments(module,subd)

    # delete module
    deletejsmmodules(module)

    # delete JMS servers
    for s in jmsservers.split(','):
        deletejmsservers(s)

    # delete JMS Pstores
    for p in pstores.split(','):
        deletejmspstores(p)

def main():
    print "Connecting to Admin"
    try:
        connect2admin()
    except Exception, e:
        print 'Could not connect to Admin'
        print e
    print 'Starting the edit session'
    edit()
    startEdit()

    HitKey=raw_input('Press any key to continue...')
    print 'Deleting the AG JMS Resources'
    try:
        deleteagjmsresources()
        print 'Done'
    except Exception, e:
        print 'Something went wrong with deleting the AG JMS Resources'
        print e

    HitKey=raw_input('Press any key to continue...')
    print 'Deleting the BPM JMS Resources'
    try:
        deletebpmjmsresources()
        print 'Done'
    except Exception, e:
        print 'Something went wrong with deleting the BPM JMS Resources'
        print e

    HitKey=raw_input('Press any key to continue...')
    print 'Deleting the PS6 JMS Resources'
    try:
        deleteps6jmsresources()
        print 'Done'
    except Exception, e:
        print 'Something went wrong with deleting the PS6 JMS Resources'
        print e

    HitKey=raw_input('Press any key to continue...')
    print 'Deleting the SOA JMS Resources'
    try:
        deletesoajmsresources()
        print 'Done'
    except Exception, e:
        print 'Something went wrong with deleting the SOA JMS Resources'
        print e

    HitKey=raw_input('Press any key to continue...')
    print 'Deleting the UMS JMS Resources'
    try:
        deleteumsjmsresources()
        print 'Done'
    except Exception, e:
        print 'Something went wrong with deleting the UMS JMS Resources'
        print e

    HitKey=raw_input('Press any key to continue...')
    activate()

main()

