#!/bin/sh
 
# SCRIPT_PATH=$(dirname $0)
SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)
 
. ${SCRIPT_PATH}/SetEnvironment.sh
 
${WL_HOME}/common/bin/wlst.sh -loadProperties ${SCRIPT_PATH}/environment.properties ${SCRIPT_PATH}/stopNodeManager.py
- See more at: http://middlewaremagic.com/weblogic/?tag=weblogic-server#sthash.Y9JY8PCP.dpuf