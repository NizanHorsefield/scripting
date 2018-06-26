#!/bin/bash

blue=$(tput setaf 4)
red=$(tput setaf 1)
normal=$(tput sgr0)


get_asg_list=$(aws autoscaling describe-auto-scaling-groups --region eu-west-1 | grep "AutoScalingGroupName" | egrep "evise-tasks-dev2|evise-submissions-dev2|evise-cpe-dev2" | awk '{print $2; }' | sed 's/"//g' | sed 's/,/ /g');

clear
printf "%40s\n${blue}These are the DEV2 Auto Scaling Groups for CPE${normal}"
for i in $get_asg_list
do
  printf "%40s\n${red}${i}${normal}"
done

printf "\n "
printf "%40s\n${blue}You can now run the FPU Exec update script against an ASG by passing it as a parameter${normal}"
printf "\n "
printf "%40s\n${red}Example: ./update_fpu_exec.sh {FPU_EXEC_VERSION} {ASG} ${normal}"
printf "\n "
printf "\n "
printf "\n "
printf "\n "
