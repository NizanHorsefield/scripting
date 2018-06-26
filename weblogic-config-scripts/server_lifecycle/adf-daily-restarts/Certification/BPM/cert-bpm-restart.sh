#!/bin/bash
###################################################
# Created by Nizan Horsefield
# Date 25th April 2017
# Version 0.1 - created and deployed
# Version 1.1 - added new function to check for FAILED managed servers.
# Version 2.0 - created for BPM
################################################################################
# This script performs the start up of 6 managed servers giving a total of 18.
# Then restarts 6 of the running managed servers
# Then shuts down the 6 it started taking the total back to 12
################################################################################
#set -x

# Variables
#NOW=$(date +"%m-%d-%Y-%H-%M-%S")
ORACLE_HOME="/opt/nextees/middleware/Oracle_SOA1"
WL_HOME="/opt/nextees/middleware/wlserver_10.3"
WLST_BIN_HOME="/opt/nextees/middleware/Oracle_SOA1/common/bin"
SCRIPT_HOME="/home/oracle/scripts/bpm-daily-restarts"
LOGGING_DIRECTORY="/home/oracle/scripts/bpm-daily-restarts/bpm-restart-logs"
LOGFILE="$LOGGING_DIRECTORY/bpm-restart.log"

# Managed server groups
GROUP_1="1"
GROUP_2="2"

# This values should be set to the number of managed servers in each group so it can be used as a success check.
# It relies on the number of managed servers per group being the same. Whch is true for EVISE Production.
SERVERCOUNT=1

# Time to sleep in between functions.
LOWSLEEP=10
MIDSLEEP=180
HIGHSLEEP=600

# Functions
function echo_log {
	NOW=$(date +"%m-%d-%Y-%H-%M-%S")
    echo ${NOW} " $1" >> ${LOGFILE}
}

function stop_managed ()
{
# This function takes a GROUP of managed servers as a variable.
# Then iterates through the list and stops each in parallel and waits for the task to complete.
# Reset the variable servers just in case
servers=""
echo_log "Stopping the BPM managed servers $1"
servers=$1
for s in $(echo ${servers} | sed "s/,/ /g")
do
    echo_log "Stopping soa_server$s"
    ${WLST_BIN_HOME}/wlst.sh ${SCRIPT_HOME}/stop-ms.py ${s} &
done
echo "waiting..."
wait
}

function start_managed ()
{
# This function takes a GROUP of managed servers as a variable.
# Then iterates through the list and starts each in parallel and waits for the task to complete.
# Reset the variable servers just in case
servers=""
echo_log "Starting the BPM managed servers $1"
servers=$1
for s in $(echo ${servers} | sed "s/,/ /g")
do
    echo_log "Starting soa_server$s"
    ${WLST_BIN_HOME}/wlst.sh ${SCRIPT_HOME}/start-ms.py ${s} &
done
echo "waiting..."
wait
}

function check_state_running ()
{
servers=$1
echo_log "Server count is $SERVERCOUNT"
unset q
for s in $(echo ${servers} | sed "s/,/ /g")
do
    state=$(${WLST_BIN_HOME}/wlst.sh getstate-ms.py ${s} | grep state | awk '{print $6}')
    if [ ${state} = 'RUNNING' ]; then
        echo_log "${s} is RUNNING";
        q=$((q+1))
    fi
done
echo_log "Up count is $q and server count is $SERVERCOUNT"
if [ ${SERVERCOUNT} -ne ${q} ]; then
        echo_log "One or more of the managed servers have failed to start. Check the logs to see what has happened"
        exit 1
    else
        echo_log "All is good. All of the managed servers seem to be up"

fi
}

function check_state_shutdown ()
{
servers=$1
echo_log "Server count is $SERVERCOUNT"
unset q
for s in $(echo ${servers} | sed "s/,/ /g")
do
    state=$(${WLST_BIN_HOME}/wlst.sh getstate-ms.py ${s} | grep state | awk '{print $6}')
    if [ ${state} = 'SHUTDOWN' ]; then
        echo_log "${s} has been SHUTDOWN";
        q=$((q+1))
    fi
done
echo_log "Shutdown count is $q and server count is $SERVERCOUNT"
if [ ${SERVERCOUNT} -ne ${q} ]; then
        echo_log "One or more of the managed servers have failed to shutdown. Check the logs to see what has happened"
        exit 1
    else
        echo_log "All is good. All of the managed servers have been shutdown"

fi
}

function check_state_failed ()
# This function will check for a failed managed server and then FORCE it down.
{
servers=$1
for s in $(echo ${servers} | sed "s/,/ /g")
do
    state=$(${WLST_BIN_HOME}/wlst.sh getstate-ms.py ${s} | grep state | awk '{print $6}')
    if [ ${state} = 'FAILED' ]; then
        echo_log "${s} is in a FAILED state so will be FORCED down";
        ${WLST_BIN_HOME}/wlst.sh ${SCRIPT_HOME}/force-stop-ms.py ${s} &
    fi
done
echo "waiting..."
wait
}


# Let's go
# Restart group 1
echo_log "##################################################"
echo_log "Restarting group 1"
stop_managed ${GROUP_1}
sleep $HIGHSLEEP
check_state_failed ${GROUP_1}
sleep $MIDSLEEP
check_state_shutdown ${GROUP_1}
sleep $LOWSLEEP
echo_log ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
start_managed ${GROUP_1}
sleep $LOWSLEEP
check_state_running ${GROUP_1}
echo_log ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
# Restart group 2
echo_log "Restarting group 2"
stop_managed ${GROUP_2}
sleep $HIGHSLEEP
check_state_failed ${GROUP_2}
sleep $MIDSLEEP
check_state_shutdown ${GROUP_2}
sleep $LOWSLEEP
echo_log ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
start_managed ${GROUP_2}
sleep $LOWSLEEP
check_state_running ${GROUP_2}
echo_log "All done :)"
exit 0
