import re
import sys
from java.lang import System
from java.lang import String
from weblogic.security.internal import SerializedSystemIni
from weblogic.security.internal.encryption import ClearOrEncryptedService
from com.estafet.fmw.platform import NullPrintStream

import wlstModule as wlst

global STATE_MAPS
STATE_MAPS = dict()

global WLSTException
WLSTException = wlst.WLSTException

global DOMAIN_DIR
DOMAIN_DIR = ""

class DevNull(NullPrintStream):
    def nothing(self):
        print ""


class DirStackEntry :
    def __init__(self, path):
        if(re.match("^/", path)) :
            self.absolutePath = path
        else:
            #build an absolute path based on the stack
            topStackEntry = getDirStack().peek()
            self.absolutePath = topStackEntry.absolutePath + "/" + path


class Stack:
    def __init__(self):
        self.__storage = []

    def isEmpty(self):
        return len(self.__storage) == 0

    def push(self,p):
        self.__storage.append(p)

    def pop(self):
        return self.__storage.pop()

    def peek(self):
        result = self.pop()
        self.push(result)
        return result

global DIR_STACK
DIR_STACK = Stack()

def newWLSTException(message):
    return wlst.WLSTException(message)

def getStateMap(name) :
    try :
        result = STATE_MAPS[name]
    except KeyError :
        result = dict()
        STATE_MAPS[name] = result
    return result

def getDirStack() :
    return DIR_STACK

def activate() :
    try :
        wlst.activate()
    except WLSTException, e:
        wlst.dumpStack()
        raise e

def assign(type, name, toType, toName) :
    return wlst.assign(type, name, toType, toName)

def cancelEdit(ans) :
    wlst.cancelEdit(ans)

def cd(path) :
    print "cd to " + path
    return wlst.cd(path)

def closeDomain() :
    wlst.closeDomain()

def connect(adminUser, password, url) :
    wlst.connect(adminUser, password, url)

def create(name, type) :
    return wlst.create(name, type)

def delete(name, type) :
    return wlst.delete(name, type)

def decrypt(encryptedText):
    encryptionService = SerializedSystemIni.getEncryptionService(DOMAIN_DIR)
    ces = ClearOrEncryptedService(encryptionService)
    clear = ces.decrypt(encryptedText)
    return clear

def decryptBytes(bytes):
    encryptionService = SerializedSystemIni.getEncryptionService(DOMAIN_DIR)
    ces = ClearOrEncryptedService(encryptionService)
    clear = ces.decryptBytes(bytes)
    return str(String(clear))

def deploy(appName, path, map):
    return wlst.deploy(appName, path, **map)


def destroyMachine(machine):
    return wlst.cmo.destroyMachine(machine)

def disconnect() :
    wlst.disconnect()

def domainConfig():
    return wlst.domainConfig()

def domainRuntime():
    return wlst.domainRuntime()

def edit() :
    wlst.edit()

def encrypt(obj) :
    return wlst.encrypt(obj, DOMAIN_DIR)

def get(name) :
    return wlst.get(name)

def getAppDeployments() :
    return wlst.cmo.getAppDeployments()

def X_getClusters() :
    return wlst.cmo.getClusters()

def getClusterNames() :
    result = []
    clusters = getClusters()
    for cluster in clusters:
        result.append(cluster.getName())
    return result

def getCluster(name) :
    clusters = getClusters()
    for cluster in clusters :
        if name == cluster.getName() :
            return cluster
    return None

def getCurrentState(obj,targetinst) :
    return wlst.cmo.getCurrentState(obj,targetinst)

def X_getMachines() :
    return wlst.cmo.getMachines()

def getMachineNames() :
    machines = getMachines()
    result = []
    for machine in machines :
        result.append(machine.getName())
    return result

def X_getMachineNamesOffline() :
    return lsmap()

def getMachine(name) :
    machines = getMachines()
    for machine in machines :
        if name == machine.getName() :
            return machine
    return None

def getMBean(path) :
    return wlst.getMBean(path)

def X_getServers() :
    return wlst.cmo.getServers()

def getServerNames() :
    result = []
    servers = getServers()
    for server in servers :
        result.append(server.getName())
    return result

def getServerRuntimes() :
    result = wlst.domainRuntimeService.getServerRuntimes()
    return result

def isRestartRequired(attr = None) :
    return wlst.isRestartRequired(attr)

def ls(propertySet) :
    return wlst.ls(propertySet)

def lsmap() :
    result = wlst.ls(returnMap='true')
    return result

def lsAttrMap() :
    result = wlst.ls(returnMap='true', returnType='a')
    return result

def lsChildMap() :
    result = wlst.ls(returnMap='true', returnType='c')
    return result

def lsOpMap() :
    result = wlst.ls(returnMap='true', returnType='o')
    return result

def nmConnect(adminUserName, adminPassword, adminListenAddress, nodemgrPort, domainName, domainDir , type, jvmArguments) :
    if jvmArguments :
        wlst.nmConnect(adminUserName, adminPassword, adminListenAddress, nodemgrPort, domainName, domainDir, nmType=type, jvmArgs=jvmArguments)
    else :
        wlst.nmConnect(adminUserName, adminPassword, adminListenAddress, nodemgrPort, domainName, domainDir, nmType=type)

def nmDisconnect() :
    wlst.nmDisconnect()

def nmKill(serverName) :
    wlst.nmKill(serverName)

def nmServerStatus(serverName) :
    return wlst.nmServerStatus(serverName)

def nmStart(serverName, domainDir) :
    wlst.nmStart(serverName, domainDir)

def popd() :
    dirStack = getDirStack()
    if not dirStack.isEmpty() :
        dirStack.pop()
        if not dirStack.isEmpty() :
            dest = dirStack.peek()
            try :
                return cd(dest.absolutePath)
            except :
                pass
    return cd("/")

def pushd(path) :
    stackEntry = DirStackEntry(path)
    getDirStack().push(stackEntry)
    try :
        dir = cd(stackEntry.absolutePath)
        return dir
    except Exception, e :
        popd()
        raise e

def pwd() :
    return wlst.pwd()

def readDomain(domainDir) :
    wlst.readDomain(domainDir)

def removeReferencesToBean(mbean) :
    wlst.editService.getConfigurationManager().removeReferencesToBean(mbean)

def save() :
    wlst.save()

def set(name, value):
    wlst.set(name, value)

def setCluster(cluster) :
    wlst.cmo.setCluster(cluster)

def setClusterMessagingMode(type) :
    wlst.cmo.setClusterMessagingMode(type)

def setFanEnabled(value) :
    wlst.cmo.setFanEnabled(value)

def setMachine(machine) :
    wlst.cmo.setMachine(machine)

def shutdown(serverName = None) :
    wlst.shutdown(name=serverName, block="true")

def startEdit() :
    wlst.startEdit()

def startNodeManager(nodemgrHome, nodemgrPort, secureListener, listenAddress, jvmArgs='-Dweblogic.security.SSL.enableJSSE=true') :
    wlst.startNodeManager(NodeManagerHome=nodemgrHome, ListenPort=nodemgrPort, SecureListener=secureListener, StartScriptEnabled='true', ListenAddress=listenAddress, jvmArgs=jvmArgs)

def unassign(sourceType, sourceName, destType, destName) :
    return wlst.unassign(sourceType, sourceName, destType, destName)

def updateDomain() :
    wlst.updateDomain()

#USE WITH CAUTION - todo - remove
def getCmo() :
    return wlst.cmo

def divert(func, location) :
    def wrapper(*args) :
        pwd = wlst.pwd()
        cd(location)
        result = func(*args)
        cd(pwd)
        return result
    return wrapper

def silent(func) :
    def wrapper(*args) :
        sysout = sys.stdout
        syserr = sys.stderr
        javaOut = System.out
        javaErr = System.err
        sys.stdout = DevNull()
        sys.stderr = DevNull()
        System.setOut(DevNull())
        System.setErr(DevNull())
        result = func(*args)
        sys.stdout = sysout
        sys.stderr = syserr
        System.setOut(javaOut)
        System.setErr(javaErr)
        return result
    return wrapper

cd = silent(cd)
ls = silent(ls)
lsmap = silent(lsmap)
domainConfig = silent(domainConfig)
domainRuntime = silent(domainRuntime)

