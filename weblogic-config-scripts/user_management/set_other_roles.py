# Author : Nizan Horsefield / Marc Eamens
# Date : 12th April 2018
# Description
import os
import getopt

from java.lang import System
from java.io import FileInputStream

def usage():
    print "Usage:"
    print "WLST_SCRIPT -p <properties> ENV(SOA/BPM/ADF) prod|nonprod"
# '-all' actions are applied to admin server in addition to managed servers
# Actions may be prefixed with "test-" to run them in test/simulation mode

#=======================================================================================
# get domain properties.
#=======================================================================================

props = Properties()
domainDir = ""
properties = ""
action = ""
serversToStart = ""
testMode = false
nonprodAccounts = {'wls_nonp_deployers': 'Deployer', 'wls_nonp_monitors': 'Monitor', 'wls_nonp_operators': 'Operator'}
prodAccounts = {'wls_prod_deployers': 'Deployer', 'wls_prod_monitors': 'Monitor', 'wls_prod_operators': 'Operator'}
environment = sys.argv[3]

properties = sys.argv[1]

propsInputStream = FileInputStream(properties)
props.load(propsInputStream)
wltype = str(sys.argv[2])
print wltype
#=======================================================================================

def connect2wls(type):
    adminUserName=props.get(type+'_adminUserName')
    adminPassword=props.get(type+'_adminPassword')
    listenAddress=props.get(type+'_listenAddress')
    listenPort=props.get(type+'_listenPort')
    environment=props.get(type+'_environment')
    domainName=props.get(type+'_domainname')
    print('=======================================================================================')
    print( 'Environment: ' + environment )
    print( 'connecting to weblogic with...')
    print( ' username: ' + adminUserName)
    print( ' password: ' + adminPassword)
    print( ' listenAddress: ' + listenAddress)
    print( ' listenPort: ' + listenPort)
    connect( adminUserName, adminPassword, 't3://'+ listenAddress + ':' + listenPort )
    print('=======================================================================================')

def addIdmGroupToRole(groupName, role, domainName):
    serverConfig()
    cd('/SecurityConfiguration/'+ domainName +'/Realms/myrealm/RoleMappers/XACMLRoleMapper')
    cmo.setRoleExpression(None, role,'Grp(' +groupName+ ')|Grp(' +role+ 's)')

if environment.lower == "nonprod":
    accounts = nonprodAccounts

if environment.lower == "prod":
    accounts = prodAccounts

connect2wls(wltype)
for group, role in nonprodAccounts.items():
    addIdmGroupToRole(group, role, domainName)

print('.')
print('.')
print('.')
print('Finished')
exit()



