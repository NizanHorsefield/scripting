#!/bin/bash
#set -x

INT_ALB_ADDRESS="dev2-evise-internal.evise-cloud.com"
EXT_ALB_ADDRESS="dev2-web.evise-cloud.com"
NameSpace=DEV2_EP_Checks

# This method takes an IP/HOST and Port then performs a netcat against it.
# It will return a 0 on success and 1 on a failure.
nc_put_metric(){
EndPoint=$1
REMOTEHOST=$2
REMOTEPORT=$3
TIMEOUT=1

    if nc -w $TIMEOUT -z $REMOTEHOST $REMOTEPORT; then
        #echo "I was able to connect to ${REMOTEHOST}:${REMOTEPORT}"
        result=1
    else
        #echo "Connection to ${REMOTEHOST}:${REMOTEPORT} failed. Exit code from Netcat was ($?)."
        result=0
    fi
    # Put Update Metric
    echo "aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace $NameSpace  --value $result --dimensions EndPoint=$EndPoint"
}

curl_put_metric(){

EndPoint=$1
URL=$2

    test=$(curl -Is ${URL} | head -1 | awk {'print $2'})
    if [ ${test} == '200' ] || [ ${test} == '405' ]; then
        result=1
    else
        result=0
    fi
    # Put Update Metric
    echo "aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace $NameSpace  --value $result --dimensions EndPoint=$EndPoint"
}

##Set out the tests below

# TCP checks 

nc_put_metric DatabasePing 10.178.233.108 1521
nc_put_metric AdfMs1Ping dev2-evise-wc-nextees1.evise-cloud.com 26820
nc_put_metric SoaMs1Ping dev2-evise-soa2-soa1.evise-cloud.com 26808
nc_put_metric OsbMs1Ping dev2-evise-soa2-osb1.evise-cloud.com 26810
nc_put_metric BpmMs1Ping dev2-evise-soa1-soa1.evise-cloud.com 26808

# URL checks
# Homepage
curl_put_metric EviseHomePageCheck https://www.evise.com

# OHS
curl_put_metric ExternalOHS http://$EXT_ALB_ADDRESS/hbeat

#UX
curl_put_metric ProfileUX http://${EXT_ALB_ADDRESS}/profile/api/ping
curl_put_metric JournalAdminUX http://${EXT_ALB_ADDRESS}/journal-admin/api/ping
curl_put_metric CoauthorUX http://${EXT_ALB_ADDRESS}/co-author/api/ping
curl_put_metric AuthorUX http://${EXT_ALB_ADDRESS}/author/api/ping
curl_put_metric TaxonomyUX http://${EXT_ALB_ADDRESS}/taxonomy/api/ping
curl_put_metric EdRevRecUX http://${EXT_ALB_ADDRESS}/editor/reviewer/recommender/api/ping
curl_put_metric EditorUX http://${EXT_ALB_ADDRESS}/editor/api/ping

# MicroServices
curl_put_metric ProfileMicroService http://$INT_ALB_ADDRESS/profile
curl_put_metric AdminProfileMicroService http://$INT_ALB_ADDRESS/admin-profile/ping
curl_put_metric SubCoauthorMicroService http://$INT_ALB_ADDRESS/submission/co-author/ping
curl_put_metric CoauthorMicroService http://$INT_ALB_ADDRESS/co-author/ping
curl_put_metric TaxonomyMicroServicehttp://$INT_ALB_ADDRESS/taxonomy/ping
curl_put_metric AuditMicroService http://$INT_ALB_ADDRESS/audit/ping
