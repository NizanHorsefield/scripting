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

def createUserfromList(list, comment):

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
    print('Creating ' + comment + ' users')
    atnr=cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider('DefaultAuthenticator');
    for objects in list.split(','):
        obj=objects.split(':')
        #obj[0] = username
        #obj[1] = password
        #obj[2] = comment
        #obj[3] = group
        try:
            print( 'Creating User : ' + obj[0] );
            atnr.createUser(obj[0],obj[1],obj[2]);
        except:
            print( obj[0] + ' account exists, skipping' );
        try:
            print( 'Adding ' + obj[0] + ' to ' + obj[3] + ' Group' );
            atnr.addMemberToGroup( obj[3], obj[0] );
        except:
            print( ' could not add to group, skipping' );
    print( 'Done ===================================');
    disconnect()

createUserfromList(props.get("adf_users"),"ADF")
createUserfromList(props.get("soa_users"),"SOA")
createUserfromList(props.get("bpm_users"),"BPM")
print('.')
print('.')
print('.')
print('Finished')
exit()



