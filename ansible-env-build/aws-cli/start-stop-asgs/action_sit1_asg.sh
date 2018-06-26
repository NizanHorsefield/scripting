#!/bin/bash
clear
echo "###############################################################################################"
echo "# This script gets the list of ASG's for SIT1. Then depending on what the user wants either   #"
echo "# sets the desired capactiy to 1 - which starts 1 instance in each ASG - effectively starting #"
echo "# sets the desired capacity to 0 - which stops 1  instance in each ASG - efectively stopping  #"
echo "###############################################################################################"
echo " "

if [ $1 = "start" ]
then 
  DES_CAP=1
fi
if [ $1 = "stop" ]
then
  DES_CAP=0
fi

action(){
#taken the action according to the user's input
get_asg_list=$(aws autoscaling describe-auto-scaling-groups --region eu-west-1 | grep "AutoScalingGroupName" | grep evise-fpu-sit1 | awk '{print $2; }' | sed 's/"//g' | sed 's/,/ /g');

#for each of the ASG#s returned set the desired capacity according to the users choice.
for i in ${get_asg_list}
do
  echo aws autoscaling set-desired-capacity --region eu-west-1 --auto-scaling-group-name ${i} --desired-capacity ${DES_CAP}
done
}

while true; do
    read -p "This script will $1 the SIT1 ASG's. OK to continue? y/n" yn
    case $yn in
        [Yy]* ) action; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

