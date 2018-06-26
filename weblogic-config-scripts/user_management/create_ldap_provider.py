# Author : Nizan Horsefield
# Date : 1st March 2018
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

def createLdapProvider(domainName):
    cmo.getSecurityConfiguration().getDefaultRealm().createAuthenticationProvider('EIDMA', 'weblogic.security.providers.authentication.LDAPAuthenticator')
    cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider('EIDMA').setControlFlag('SUFFICIENT')
    cd('/SecurityConfiguration')
    cd(domainName)
    cd('Realms/myrealm/AuthenticationProviders')
    cd('EIDMA')
    cmo.setHost('idm.evise-nonprod.com')
    cmo.setPort(389)
    cmo.setPrincipal('uid=svc_weblogic,cn=users,cn=accounts,dc=evise-nonprod,dc=com')
    cmo.setCredential('yLYRP9kJTzZM5Fb4VRLJ5xccwJWz26um')

    # Group Info
    cmo.setGroupBaseDN('cn=groups,cn=accounts,dc=evise-nonprod,dc=com')
    cmo.setAllGroupsFilter('(&(cn=*)(|(objectclass=posixGroup)))')
    cmo.setGroupFromNameFilter('(&(cn=%g)(objectclass=posixGroup))')
    cmo.setGroupSearchScope('subtree')
    cmo.setGroupMembershipSearching('unlimited')
    cmo.setMaxGroupMembershipSearchLevel(5)
    cmo.setStaticGroupNameAttribute('cn')
    cmo.setStaticGroupObjectClass('posixgroup')
    cmo.setStaticMemberDNAttribute('member')
    cmo.setStaticGroupDNsfromMemberDNFilter('(&(member=%M)(objectclass=posixgroup))')
    
    # User Info
    cmo.setUserBaseDN('cn=users,cn=accounts,dc=evise-nonprod,dc=com')
    cmo.setUserFromNameFilter('(&(uid=%u)(objectclass=person))')
    cmo.setUserSearchScope('subtree')
    cmo.setUserNameAttribute('uid')

    print( 'Done ===================================');

def updateDefaultAuthenticator(flag,domainName):
    cd('/SecurityConfiguration/'+ domainName +'/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
    cmo.setControlFlag(flag)

connect2wls(wltype)
edit()
cancelEdit('y')
startEdit()
createLdapProvider(domainName)
updateDefaultAuthenticator('SUFFICIENT',domainName)
save()
activate()

print('.')
print('.')
print('.')
print('Finished')
exit()



