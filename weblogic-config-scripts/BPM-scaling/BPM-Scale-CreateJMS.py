#==========================================================================
# FileName      : BPM-Scale-CreateJMS.py
# Updated       : 18/04/2017
# Author        : Nizan Horsefield
# Description:
# This simple script will create JMS server, Pstore and target the SubD
#==========================================================================

import sys
print "@@@ Starting the script ..."
from java.util import *
from javax.management import *

# ingredients
def connect2admin():
    adminURL='t3://sit2-evise-soa1-adminserver.evise-cloud.com:7001'
    adminUserName='weblogic'
    adminPassword='getrdone1''
    connect(adminUserName, adminPassword, adminURL)

##############################################################################################################
# re-usable routine to create JMS Server and Modules

def genjmssrvrlist(prefix,until):
    # routine to generate an array that contains a list of JMS server names from a given prefix.
    # the 'until' tells range to generate numbers up to, but not including this number
    jmsserverlist = []
    for r in range(1,until):
        s='com.bea:Name='+prefix+str(r)+',Type=JMSServer'
        jmsserverlist.append(ObjectName(str(s)))
    return jmsserverlist

def createfilepstore(pstorename,dirname,managedserver):
    # E.g. createfilepstore('AGJMSServerJDBCStore_auto_3','/home/domain/fs','soa_server3')
    # create the JDBC Pstore
    try:
        print 'Creating '+pstorename
        cd('/')
        cmo.createFileStore(pstorename)
        cd('/FileStores/'+pstorename)
        cmo.setDirectory(dirname)
        cmo.addTarget(getMBean("/Servers/"+managedserver))
        print "Done"
    except Exception, e:
        print 'Could not create '+pstorename
        print e

def createjdbcpstore(pstorename,datasourcename,prefix,managedserver):
    # E.g. createjdbcpstore('AGJMSServerJDBCStore_auto_3','JMSDataSource','soa_server3')
    # create the JDBC Pstore
    try:
        print 'Creating '+pstorename
        cd('/')
        cmo.createJDBCStore(pstorename)
        cd('/JDBCStores/'+pstorename)
        cmo.setDataSource(getMBean('/SystemResources/'+datasourcename))
        cmo.setPrefixName(prefix)
        set('Targets',jarray.array([ObjectName('com.bea:Name='+managedserver+',Type=Server')], ObjectName))
        print "Done"
    except Exception, e:
        print 'Could not create '+pstorename
        print e

def createjmsserver(jmsservername,managedserver,pstorename):
    # createjmsserver('AGJMSServer_auto_4','soa_server4','AGJMSFileStore_auto_4')
    try:
        print 'Creating '+jmsservername+ ' with '+pstorename
        cd('/')
        cmo.createJMSServer(jmsservername)
        cd('/JMSServers/'+jmsservername)
        cmo.addTarget(getMBean('/Servers/'+managedserver))
        print "Done"
    except Exception, e:
        print 'Could not create '+jmsservername
        print e

        # Now set persistent store for the JMS server
    try:
        print 'Assign '+pstorename+ ' to ' +jmsservername
        cd('/Deployments/'+jmsservername)
        cmo.setPersistentStore(getMBean('/FileStores/'+pstorename))
        #cmo.setPersistentStore(getMBean('/JDBCStores/'+PstoreName))
        print "Done"
    except Exception, e:
        print 'Could not assign '+pstorename
        print e

def targetsubdeployments(jmsmodulename,subdeployment,jmsserverprefix):
    # E.g. targetsubdeployments('AGJMSModuleUDDs','AGJMSSubDM','AGJMSServer_auto_')
    try:
        print 'Targeting '+subdeployment+ ' to the fill list of JMS Servers'
        cd('/SystemResources/'+jmsmodulename+'/SubDeployments/'+subdeployment)
        list = genjmssrvrlist(jmsserverprefix,6)
        set('Targets',jarray.array(list, ObjectName))
        print "Done"
    except Exception, e:
        print 'Could not target '+subdeployment
        print e
##############################################################################################################

# recipe
def main():
    connect2admin()
    edit()
    startEdit()
    # create the PStores
    for i in range(1,5): # this use of the range() takes two parameters - the starting number and the max value ( which is not used)
        try:
            createfilepstore('FileStore'+str(i),'/home/vagrant/Oracle/Middleware/user_projects/domains/webcenter_domain/fs','nexteesadf_server'+str(i))
        except:
            print 'Filestore creation failed...'+'machine'+str(i)
    HitKey=raw_input('Press any key to continue...')
    # create the JMS Servers
    for i in range(1,5): # this use of the range() takes two parameters - the starting number and the max value ( which is not used)
        try:
            createjmsserver('JMSServer'+str(i),'nexteesadf_server'+str(i),'FileStore'+str(i))
        except:
            print 'JMS Server creation failed...'+'machine'+str(i)
    save()
    activate()
    HitKey=raw_input('Press any key to continue...')
    edit()
    startEdit()
    targetsubdeployments('AGJMSModule','AGJMSSubDM','AGJMSServer_auto_')
    targetsubdeployments('BPMJMSModule','BPMJMSSubDM','BPMJMSServer_auto_')
    targetsubdeployments('EviseSOAJMSModule','AGJMSSubDM','AGJMSServer_auto_')
    targetsubdeployments('PS6SOAJMSModule','AGJMSSubDM','AGJMSServer_auto_')
    targetsubdeployments('SOAJMSModule','AGJMSSubDM','AGJMSServer_auto_')
    targetsubdeployments('UMSJMSSystemResource','AGJMSSubDM','AGJMSServer_auto_')
    HitKey=raw_input('Press any key to continue...')
    save()
    activate()
    print "All Done"

# cook
main()
