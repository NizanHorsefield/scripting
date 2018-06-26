#!/bin/bash
# This is mock up script that puts random values into CW to allow a mock up dashbaord to be created that shows submission data

WORKING_DIR="/home/oracle/scripts/admin-scripts/cloudwatch/wl-custom-metrics"
AWS_EXEC="/usr/bin/aws"

AverageSubmissionPerHour=$((RANDOM%100))
DecisionsMade=$((RANDOM%50))
InvitationsSent=$((RANDOM%250))

echo "$AWS_EXEC cloudwatch put-metric-data --region eu-west-1 --metric-name AverageSubmissionPerHour --namespace SubmissionsKPI --unit Count --value ${AverageSubmissionPerHour} --dimensions Environment=PROD"

echo "$AWS_EXEC cloudwatch put-metric-data --region eu-west-1 --metric-name DecisionsMade --namespace SubmissionsKPI --unit Count --value ${DecisionsMade} --dimensions Environment=PROD"

echo "$AWS_EXEC cloudwatch put-metric-data --region eu-west-1 --metric-name InvitationsSent --namespace SubmissionsKPI --unit Count --value ${InvitationsSent} --dimensions Environment=PROD"
