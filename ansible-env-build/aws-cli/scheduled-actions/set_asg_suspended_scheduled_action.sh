#!/bin/bash
clear
echo "###########################################################################################################################"
echo "# This script gets the list of ASG's for the environment you choose, then adds scheduled actions as a SuspenedProcess.    #"
echo "###########################################################################################################################"
echo " "

action(){
#taken the action according to the user's input
get_asg_list=$(aws autoscaling describe-auto-scaling-groups --region eu-west-1 | grep "AutoScalingGroupName" | grep $1 | awk '{print $2; }' | sed 's/"//g' | sed 's/,/ /g');
#for each of the ASG#s returned set the scheduled actions
for i in ${get_asg_list}
do
  echo "Adding scheduled-action-name to SuspenedProcesses for $i"
  aws autoscaling suspend-processes --auto-scaling-group-name ${i} --scaling-processes ScheduledActions
  echo "#####"

done
}

PS3='Please choose the environment you wish to change: '
options=("dev" "dev2" "sit1" "sit2" "cert" "quit")
select opt in "${options[@]}"
do
    case $opt in
        "dev2")
            echo "you chose ${opt}-"
            action ${opt}-; break
            ;;
        "sit2")
            echo "you chose ${opt}-"
            action ${opt}-; break
            ;;
        "cert")
            echo "you chose ${opt}-"
            action ${opt}-; break
            ;;
        "quit")
            break
            ;;
        *) echo invalid option;;
    esac
done
