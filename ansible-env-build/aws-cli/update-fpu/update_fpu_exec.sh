#!/bin/bash
########################################################################################################################
# This script will copy a given FPUExec Jar file from S3 to NFS, update the TAGS in the relevant ASG, then terminate   #
# the EC2 instances so that new ones are created.                                                                      #
########################################################################################################################
#Set VARS


blue=$(tput setaf 4)
red=$(tput setaf 1)
green=$(tput setaf 2)
normal=$(tput sgr0)

#set -x
FPUEXEC_VERSION=$1
FPUEXEC_JAR=fpu-exec-$1.jar
FPUEXEC_SRC=s3://evise-fpu-deployment/common/exec/releases/com/elsevier/evise/fpu-exec/${FPUEXEC_VERSION}/${FPUEXEC_JAR}
FPUEXEC_DEST=/tmp/fpu/exec

FPUASGLIST=$2

# step 1
updateasgtag() {
#Update the FPUExec TAG in the ASGs in the list
for i in ${FPUASGLIST}
  do
    aws autoscaling create-or-update-tags --tags --region eu-west-1 ResourceId=${i},ResourceType=auto-scaling-group,Key=FPUExec,Value=${FPUEXEC_JAR},PropagateAtLaunch=true
  done
  printf "%40s\n${green}Tags Updated${normal}"
  printf "\n"
}

# step 3
terminateec2() {
#Terminate instances to force the creation of new ones.
printf "%40s\n${blue}Now cycling the instances${normal}"
printf "\n"
for i in ${FPUASGLIST}
do
  for ID in $(aws autoscaling describe-auto-scaling-instances --region eu-west-1 --query 'AutoScalingInstances[?AutoScalingGroupName==`'${i}'`]' --output text | awk '{ print $4; }');
   do
    echo aws autoscaling terminate-instance-in-auto-scaling-group --region eu-west-1 --instance-id ${ID} --no-should-decrement-desired-capacity
   done
done
  printf "%40s\n${green}All Done!${normal}"
  printf "\n"
}

# step 2
copyfroms3tonfs() {
#Copy the FPU Exec jar from S3 to NFS
printf "%40s\n${blue}Copying  ${FPUEXEC_SRC} to ${FPUEXEC_DEST}${normal}"
printf "\n"
aws s3 cp ${FPUEXEC_SRC} ${FPUEXEC_DEST}
if [ -f  ${FPUEXEC_DEST}/${FPUEXEC_JAR} ]
then
    printf "%40s\n${blue}FPU Exec copied to NFS now updating the ASG Tags${normal}"
    updateasgtag
    terminateec2
else
    printf "%40s\n${red}Something went wrong with the copy${normal}"
fi
}

#Check version is set
if [ -z ${FPUEXEC_VERSION+x} ];
  then
    printf "%40s\n${red}Please set the FPU Exec version${normal}"
    exit 1
  else
    printf "%40s\n${blue}FPU Version is set to ${green}${FPUEXEC_VERSION}${normal}"
    printf "\n"
    #start
    copyfroms3tonfs
fi
