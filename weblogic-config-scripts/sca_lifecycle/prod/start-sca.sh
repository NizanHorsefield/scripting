#!/usr/bin/env bash

SOA_URL="prod-evise-soa2-soa1.evise-cloud.com"
SOA_PORT="26808"
USERNAME="weblogic"
PASSWORD="letmeinnow1"
COMPOSITE_NAME="ManageVTWAssetUploadService"
REVISION="15.0"

WLST_HOME="/opt/nextees/middleware/Oracle_SOA1/common/bin"
SCRIPT_HOME="/home/oracle/scripts/wlst/sca-control"

#Execute

$WLST_HOME/wlst.sh $SCRIPT_HOME/start-sca.py ${SOA_URL} ${SOA_PORT} ${USERNAME} ${PASSWORD} ${COMPOSITE_NAME} ${REVISION}