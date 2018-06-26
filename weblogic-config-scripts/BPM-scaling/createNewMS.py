#==========================================================================
# FileName      : CreateNewMS.py
# Updated       : 18/04/2017
# Author        : Nizan Horsefield
# Description:
# This simple script will create multiple machines
# set the NodeManager properties, and create managed servers as clones.
#==========================================================================

import sys
print "@@@ Starting the script ..."
from java.util import *
from javax.management import *

def connect2admin():
    adminURL='t3://192.168.33.55:7001'
    adminUserName='weblogic'
    adminPassword='password123'
    connect(adminUserName, adminPassword, adminURL)

def printmachinelist():
    cd('/')
    redirect('/dev/null', toStdOut='false')
    machineslist=ls('Machines',returnMap='true')
    for m in machineslist: print m
    stopRedirect()

def createmachine(machinename, machineip,nmport):
    # Create Node Managed Server
    try:
        print "Creating Node Manager " +machinename
        cd('/')
        create(machinename, 'UnixMachine')
        cd('/Machines/'+machinename+'/NodeManager/'+machinename)
        cmo.setNMType('Plain')
        cmo.setListenAddress(machineip)
        cmo.setListenPort(nmport)
        cmo.setDebugEnabled(false)
    except Exception, e:
        print 'Node Manager creation failed...'+machinename
        print e

def createmanagedserver(typename,iteration,listenaddress,port,nodemanager):
    # Create Managed Server
    servername = typename+'_server'+iteration

    try:
        print "Creating Managed Server " +servername
        cd('/')
        cmo.createServer(servername)
        cd('/Servers/' + servername)
        cmo.setListenAddress(listenaddress)
        cmo.setListenPort(port)
        cmo.setMachine(getMBean('/Machines/' + nodemanager))
        cmo.setCluster(getMBean('/Clusters/'+typename+'_cluster'))
        print "Created Managed Server " +servername
    except Exception, e:
        print 'Manager Server creation failed...'+servername
        print e

def main():
    connect2admin()
    print "Before machines creation..."
    edit()
    startEdit()
    printmachinelist()
    HitKey=raw_input('Press any key to continue...')
    # the for loop creates a number of NMs in one go.
    for i in range(3,5): # this use of the range() takes two parameters - the starting number and generate numbers up to, but not including this number
        try:
           createmachine('soaosb_nm'+str(i),'dev2-evise-wc-nm'+str(i)+'.evise-cloud.com',5556)
        except Exception, e:
           print 'Machine creation failed...'+'machine'+str(i)
           print e
    save()
    activate()
    print "After creation..."
    printmachinelist()
    HitKey=raw_input('Press any key to continue...')
    edit()
    startEdit()
    # the for loop creates a number of NMs for each NM in one go.
    for i in range(3,5): # this use of the range() takes two parameters - the starting number and generate numbers up to, but not including this number
        try:
            createmanagedserver('soa',+str(i),'sit2-evise-soa1-soa'+str(i)+'.evise-cloud.com',26809,'soaosb_nm2')
        except Exception, e:
            print 'Managed server creation failed...'+'sit2-evise-soa1-soa'+str(i)
            print e
    for i in range(3,5): # this use of the range() takes two parameters - the starting number and generate numbers up to, but not including this number
        try:
            createmanagedserver('soa',+str(i),'sit2-evise-soa1-soa'+str(i)+'.evise-cloud.com',26809,'soaosb_nm3')
        except Exception, e:
            print 'Managed server creation failed...'+'sit2-evise-soa1-soa'+str(i)
            print e
    save()
    activate()

main()