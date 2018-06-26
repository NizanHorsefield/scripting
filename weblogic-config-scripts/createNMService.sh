#!/bin/sh
#
# chkconfig: 235 91 35
# description: starts and stops the node manager
#
#
. /etc/rc.d/init.d/functions
 
RETVAL=0
SERVICE="nodemanager"
 
start() {
    echo "Starting Node Manager"
    su - weblogic -c "/home/weblogic/weblogic12.1.1/scripts/NodeManagerStartService.sh" >/dev/null 2>&1
    RETVAL=$?
    [ $RETVAL -eq 0 ] && success || failure
    echo
    [ $RETVAL -eq 0 ] && touch /var/lock/subsys/${SERVICE}
    return $RETVAL
}
 
stop() {
    echo "Stopping Node Manager"
    su - weblogic -c "/home/weblogic/weblogic12.1.1/scripts/NodeManagerStopService.sh" >/dev/null 2>&1
    RETVAL=$?
    [ $RETVAL -eq 0 ] && success || failure
    echo
    [ $RETVAL -eq 0 ] && rm -r /var/lock/subsys/${SERVICE}
    return $RETVAL
}
 
restart() {
    stop
    start
}
 
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo $"Usage: $0 {start|stop|restart}"
        exit 1
esac
 
exit $?