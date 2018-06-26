#!/bin/bash
# This script takes two command line parameters -
## 1 -  ENV which can be dev1, dev2, sit1, sit2, cert or prod
## 2 - USE which can be ADF, SOA or BPM

# Usage
## ./putJvmMetricsToCw.sh ENV USE
## E.g.  ./putJvmMetricsToCw.sh dev1 ADF

# Preparation
## The WORKING_DIR needs to be set to the directory that contains the WLST script
## Within this folder should be one called properties containing the property files, and a symlink to the WL_HOME/common/bin folder
## so that wlst.sh can be accessed.

WORKING_DIR="/home/oracle/scripts/admin-scripts/cloudwatch/wl-custom-metrics"
AWS_EXEC="/usr/bin/aws"

OIFS=$IFS;
IFS=",";

ENV=$1
USE=$2

servers=`cat $WORKING_DIR/properties/managed_servers.$ENV`
serversArray=$servers;

for server in $serversArray
    do
        # Get JVM Metric data
        # hogging, stuck, heap, state

        metrics=$($WORKING_DIR/wlst_home/wlst.sh $WORKING_DIR/getJvmMetrics-v2.py $WORKING_DIR/properties/$ENV.properties $server | grep jvmmetrics)

        # split result into an array
        IFS=', ' read -r -a metricsArray <<< "$metrics"

        #read array objects and pass to script vars
        HoggingThreadNum=${metricsArray[1]}
        StuckThreadNum=${metricsArray[2]}
        HeapPercentage=${metricsArray[3]}
        JvmState=${metricsArray[4]}

         # Put Cloudwatch Custom Metric data
        if [ "${HoggingThreadNum}" != "" ]; then
        $AWS_EXEC cloudwatch put-metric-data --region eu-west-1 --metric-name JvmHoggingThreadCount --namespace JvmMetrics --unit Count --value ${HoggingThreadNum} --dimensions JvmId=${server},JvmType=Oracle,JvmUse=${USE},Environment=${ENV}
        fi

        if [ "${HeapPercentage}" != "" ]; then
        $AWS_EXEC cloudwatch put-metric-data --region eu-west-1 --metric-name JvmHeapUsage --namespace JvmMetrics --unit Percent --value ${HeapPercentage} --dimensions JvmId=${server},JvmType=Oracle,JvmUse=${USE},Environment=${ENV}
        fi

        if [ "${StuckThreadNum}" != "" ]; then
        $AWS_EXEC cloudwatch put-metric-data --region eu-west-1 --metric-name JvmStuckThreadCount --namespace JvmMetrics --unit Count --value ${StuckThreadNum} --dimensions JvmId=${server},JvmType=Oracle,JvmUse=${USE},Environment=${ENV}
        fi

        if [ "${JvmState}" != "" ]; then
        $AWS_EXEC cloudwatch put-metric-data --region eu-west-1 --metric-name JvmState --namespace JvmMetrics --unit Count --value ${JvmState} --dimensions JvmId=${server},JvmType=Oracle,JvmUse=${USE},Environment=${ENV}
        fi

    done

IFS=$OIFS;