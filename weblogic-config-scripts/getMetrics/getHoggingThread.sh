#!/bin/bash
WLST_BIN_HOME="/home/ec2-user/Oracle/Middleware/wlserver_10.3/common/bin"

GROUP_1="1,2,3,4,5"

function get_htc ()
{
# This function takes a GROUP of managed servers as a variable.
# Then iterates through the list and starts each in parallel and waits for the task to complete.
# Reset the variable servers just in case
servers=""
echo_log "Starting the nexteesadf managed servers $1"
servers=$1
for s in $(echo ${servers} | sed "s/,/ /g")
do
    echo_log "Starting nexteesadf_server$s"
    ${WLST_BIN_HOME}/wlst.sh ${SCRIPT_HOME}/start-ms.py ${s}
done
}

get_htc $GROUP_1