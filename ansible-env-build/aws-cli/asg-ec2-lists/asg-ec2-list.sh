#!/bin/bash
for i in `aws autoscaling describe-auto-scaling-groups --region eu-west-1 --auto-scaling-group-name $1 | grep -i instanceid  | awk '{ print $2}' | cut -d',' -f1| sed -e 's/"//g'`
do
aws ec2 describe-instances --instance-ids $i | grep -i PrivateIpAddress | awk '{ print $2 }' | head -1 | cut -d"," -f1
done;
