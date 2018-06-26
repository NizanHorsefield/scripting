#!/bin/bash
#set -x

INT_ALB_ADDRESS="dev2-evise-internal.evise-cloud.com"
EXT_ALB_ADDRESS="dev2-web.evise-cloud.com"

# This method takes an IP/HOST and Port then performs a netcat against it.
# It will return a 0 on success and 1 on a failure.
nc_put_metric(){
NameSpace=$1
EndPoint=$2
REMOTEHOST=$3
REMOTEPORT=$4

TIMEOUT=1

    if nc -w$TIMEOUT -z $REMOTEHOST $REMOTEPORT; then
        #echo "I was able to connect to ${REMOTEHOST}:${REMOTEPORT}"
        result=1
    else
        #echo "Connection to ${REMOTEHOST}:${REMOTEPORT} failed. Exit code from Netcat was ($?)."
        result=0
    fi
    # Put Update Metric
    echo aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace $NameSpace  --value $result --dimensions EndPoint=$EndPoint
}

curl_put_metric(){
NameSpace=$1
EndPoint=$2
URL=http://$3$4

    test=$(curl -Is ${URL} | head -1 | awk {'print $2'})
    if [ ${test} == '200' ] || [ ${test} == '405' ]; then
        result=1
    else
        result=0
    fi
    # Put Update Metric
    echo aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace $NameSpace  --value $result --dimensions EndPoint=$EndPoint
}

##Set out the tests below

# Take each line of targets.txt andi check for HTTP response code and total time using curl
while read NameSpace Location EndPoint URI
do
    if [ ${Location} == 'External' ]; then
        ALB_ADDRESS=${EXT_ALB_ADDRESS}
    elif [ ${Location} == 'Internal' ]; then
        ALB_ADDRESS=${INT_ALB_ADDRESS}
    else
        echo "Unknown parameter"
    fi

	curl_put_metric ${NameSpace} ${EndPoint} ${ALB_ADDRESS} ${URI}
done < curl_dev2_targets.txt


# Take each line of targets.txt andi check for HTTP response code and total time using curl
while read NameSpace EndPoint Host Port
do
	nc_put_metric ${NameSpace} ${EndPoint} ${Host} ${Port}
done < nc_dev2_targets.txt