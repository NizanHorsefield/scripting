#!/bin/bash
WLST_BIN_HOME="/home/ec2-user/Oracle/Middleware/wlserver_10.3/common/bin"
SCRIPT_HOME="/home/ec2-user/scripts"
GROUP_1="1,2,3,4,5"
set -x
function get_htc ()
{
	# This function takes a GROUP of managed servers as a variable.
	# Then iterates through the list and starts each in parallel and waits for the task to complete.
	# Reset the variable servers just in case
	servers=""
	#echo_log "Starting the nexteesadf managed servers $1"
	servers=$1
	for s in $(echo ${servers} | sed "s/,/ /g")
	do
          #echo_log "Starting nexteesadf_server$s"
	  HTC=$(${WLST_BIN_HOME}/wlst.sh ${SCRIPT_HOME}/getHTC.py ${s} | ../wl-custom-metrics/grep HTC | awk '{print $2}')
	  if [ ! -z "${HTC}" ]; then
	  #echo_log "${s} is RUNNING";
	    echo "HTC is " $HTC
	    python ${SCRIPT_HOME}/test-custom-metrics.py $HTC nexteesadf_server$s
	  fi	
	done
}

get_htc $GROUP_1
