# Author : Nizan Horsefield
# Date : 8th December 2017
# Description
import os
import getopt

from java.lang import System
from java.io import FileInputStream

def usage():
    print "Usage:"
    print "WLST_SCRIPT -p <properties>"
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

try:
    opts, args    = getopt.getopt(sys.argv[1:], "p:")
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)

for opt, arg in opts:
    if opt == "-p":
        properties = arg

if properties == "":
    print "Missing \"-p Property File\" parameter."
    usage()
    sys.exit(2)

propsInputStream = FileInputStream(properties)
props.load(propsInputStream)
#=======================================================================================

def listServers():
    servers = cmo.getServers()

    for server in servers:
        print 'Server is ' + server.getName()

def changeUserPassword(list, comment, domainName):

    adminUserName=props.get(comment+'_adminUserName')
    adminPassword=props.get(comment+'_adminPassword')
    listenAddress=props.get(comment+'_listenAddress')
    listenPort=props.get(comment+'_listenPort')
    environment=props.get(comment+'_environment')
    print('=======================================================================================')
    print( 'Environment: ' + environment )
    print( 'connecting to weblogic with...')
    print( ' username: ' + adminUserName)
    print( ' password: ' + adminPassword)
    print( ' listenAddress: ' + listenAddress)
    print( ' listenPort: ' + listenPort)
    connect( adminUserName, adminPassword, 't3://'+ listenAddress + ':' + listenPort )
    print('=======================================================================================')
    print('Changing ' + comment + ' user passwords')
    cd('/SecurityConfiguration/'+ domainName +'/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
    for objects in list.split(','):
        obj=objects.split(':')
        #obj[0] = username
        #obj[1] = password
        #obj[2] = comment
        #obj[3] = group
        try:
            print( 'Changin password for : ' + obj[0] );
            cmo.resetUserPassword(obj[0],obj[1])
        except:
            print( "Couldn't change the password for " + obj[0] );
    print( 'Done ===================================');
    disconnect()

#changeUserPassword(props.get("adf_users"),"ADF", "base_domain")
changeUserPassword(props.get("soa_users"),"SOA", "soaosb_domain")
changeUserPassword(props.get("bpm_users"),"BPM", "soaosb_domain")
print('.')
print('.')
print('.')
print('Finished')
exit()



