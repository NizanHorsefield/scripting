#!/bin/bash
#set -x

GROUP_1="1,2,3,4,5,6"

function stop-managed ()
{
	# This function takes a GROUP of managed servers as a variable.
	# Then iterates through the list and stops the managed server
	# Reset the variable serves just in case
	servers=""
	echo "Stopping the managed servers"
	servers=$1
	for s in $(echo $servers | sed "s/,/ /g") 
	do
		    echo "Stopping $s"
		        #${WLST_BIN_HOME}/wlst.sh ${SCRIPT_HOME}/stop-ms.py ${s} &
			var=$((var+1))
			sleep 1$s &
		done
		wait
		if [ $var=6 ]; then  
			$check="All is Good" 
		else
			$check="All is not good"
		fi

		if [ ${check} == "All is Good" ]; then
			echo "GOOD!"
		fi
	}


stop-managed $GROUP_1

