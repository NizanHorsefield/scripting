#!/bin/bash
clear
echo "###############################################################################################"
echo "# This script gets the list of ASG's for DEV. Then depending on what the user wants either   #"
echo "# sets the desired capactiy to 1 - which starts 1 instance in each ASG - effectively starting #"
echo "# sets the desired capacity to 0 - which stops 1  instance in each ASG - efectively stopping  #"
echo "###############################################################################################"
echo " "

if [ $1 = "start" ]
then 
  CAPACITY=1
fi
if [ $1 = "stop" ]
then
  CAPACITY=0
fi

SEARCH_STRING=$2

action(){
get_asg_list_2=$(aws autoscaling describe-auto-scaling-groups --region eu-west-1 | grep "AutoScalingGroupName" | grep ${SEARCH_STRING} | awk '{print $2; }' | sed 's/"//g' | sed 's/,/ /g');

for i in ${get_asg_list_2}
do
  aws autoscaling update-auto-scaling-group --auto-scaling-group-name ${i} --min-size ${CAPACITY} --max-size ${CAPACITY} --desired-capacity ${CAPACITY}
done
}

while true; do
    read -p "This script will $1 the ${SEARCH_STRING} ASG's. enter stop/start SEARCH_STRING - OK to continue? y/n - " yn
    case $yn in
        [Yy]* ) action; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

