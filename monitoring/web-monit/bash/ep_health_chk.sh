#!/bin/bash
#set -x

INT_ALB_ADDRESS="dev2-evise-internal.evise-cloud.com"
EXT_ALB_ADDRESS="dev2-web.evise-cloud.com"

# This method takes an IP/HOST and Port then performs a netcat against it.
# It will return a 0 on success and 1 on a failure.
nc_test(){
REMOTEHOST=$1
REMOTEPORT=$2
TIMEOUT=1
    if nc -w $TIMEOUT -z $REMOTEHOST $REMOTEPORT; then
        #echo "I was able to connect to ${REMOTEHOST}:${REMOTEPORT}"
        return 1
    else
        #echo "Connection to ${REMOTEHOST}:${REMOTEPORT} failed. Exit code from Netcat was ($?)."
        return 0
    fi
}

# This method takes an URL then performs a wget request against it.
# It will return a 0 on success and 1 on a failure.
w_url_test(){
URL=$1
    wget -S --spider $URL 2>&1 | awk '/^  /'
    if [ $? -ne 0 ]; then
        echo "Server is UP"
    else
        echo "Server is down"
    fi
}

# This method takes an URL then performs a curl request against it.
# It will return a 0 on success and 1 on a failure.
c_url_test(){
URL=$1
    test=$(curl -Is ${URL} | head -1 | awk {'print $2'})
    if [ ${test} == '200' ] || [ ${test} == '405' ]; then
        return 1
    else
        return 0
    fi
}

test_put_metric(){

NameSpace=$1
URL=$2
EndPoint=$3

    test=$(curl -Is ${URL} | head -1 | awk {'print $2'})
    if [ ${test} == '200' ] || [ ${test} == '405' ]; then
        result=1
    else
        result=0
    fi
    # Put Update Metric
    aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace $NameSpace  --value $result --dimensions EndPoint=$EndPoint
}


evise_home_page=$(c_url_test DEV2_EP_Checks https://www.evise.com EviseHomePageCheck )
#aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=EviseHomePageCheck





##Set out the test below

result1=$(nc_test 10.178.233.108 1521)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=DatabasePing

result2=$(nc_test dev2-evise-wc-nextees1.evise-cloud.com 26820)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=AdfMs1Ping

result3=$(nc_test dev2-evise-soa2-soa1.evise-cloud.com 26808)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=SoaMs1Ping

result4=$(nc_test dev2-evise-soa2-osb1.evise-cloud.com 26810)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=OsbMs1Ping

result5=$(nc_test dev2-evise-soa1-soa1.evise-cloud.com 26808)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=BpmMs1Ping

evise_home_page=$(c_url_test https://www.evise.com)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=EviseHomePageCheck

# OHS
dev2_eohs_endpoint=$(c_url_test http://$EXT_ALB_ADDRESS/hbeat)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=ExternalOHS

#UX
dev2_profile_endpoint=$(c_url_test http://${EXT_ALB_ADDRESS}/profile/api/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=ProfileUX

dev2_journal_admin_endpoint=$(c_url_test http://${EXT_ALB_ADDRESS}/journal-admin/api/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=JournalAdminUX

dev2_coauthor_endpoint=$(c_url_test http://${EXT_ALB_ADDRESS}/co-author/api/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=CoauthorUX

dev2_author_endpoint=$(c_url_test http://${EXT_ALB_ADDRESS}/author/api/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=AuthorUX

dev2_taxonomy_endpoint=$(c_url_test http://${EXT_ALB_ADDRESS}/taxonomy/api/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=TaxonomyUX

dev2_ed_rev_rec_endpoint=$(c_url_test http://${EXT_ALB_ADDRESS}/editor/reviewer/recommender/api/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=EdRevRecUX

dev2_editor_endpoint=$(c_url_test http://${EXT_ALB_ADDRESS}/editor/api/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=EditorUX

# MicroServices
dev2_profile_endpoint=$(c_url_test http://$INT_ALB_ADDRESS/profile/)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=ProfileMicroService

dev2_admin_profile_endpoint=$(c_url_test http://$INT_ALB_ADDRESS/admin-profile/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=AdminProfileMicroService

dev2_sub_coauthor_endpoint=$(c_url_test http://$INT_ALB_ADDRESS/submission/co-author/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=SubCoauthorMicroService

dev2_coauthor_endpoint=$(c_url_test http://$INT_ALB_ADDRESS/co-author/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=CoauthorMicroService

dev2_taxonomy_endpoint=$(c_url_test http://$INT_ALB_ADDRESS/taxonomy/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=TaxonomyMicroService

dev2_audit_endpoint=$(c_url_test http://$INT_ALB_ADDRESS/audit/ping)
aws cloudwatch put-metric-data --region eu-west-1 --metric-name health_check --namespace DEV2_EP_Checks  --value $? --dimensions EndPoint=AuditMicroService
