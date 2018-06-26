#!/bin/bash
#set -x

# Take each line of targets.txt andi check for HTTP response code and total time using curl
while read NAME NAMESPACE URL
do
	read -r RESPONSE RUNTIME <<<$(curl -m 3 -Is -o /dev/null -w '%{response_code} %{time_total}' ${URL})
	echo "ResponseCode=$RESPONSE - $NAME - Namespace=$NAMESPACE (URL=$URL) - $RUNTIME"
#       aws cloudwatch put-metric-data --metric-name health_check --namespace $NAMESPACE --value $RESPONSE --dimensions Name=$NAME
done < targets.txt
