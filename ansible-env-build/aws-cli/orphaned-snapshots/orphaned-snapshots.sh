#!/bin/bash

#for s in $(comm -23 <(echo $(aws ec2 describe-snapshots --region eu-west-1 | grep SNAPSHOT | awk '{print $2}' | sort | uniq) | tr ' ' '\n') <(echo $(aws ec2 describe-images --region eu-west-1 | grep BLOCKDEVICEMAPPING | awk '{print $3}' | sort | uniq) | tr ' ' '\n') | tr '\n' ' ')
#do
#  echo Deleting snapshot $s
  #ec2-delete-snapshot --region eu-west-1 $s 
#done

comm -23 <(aws ec2 describe-snapshots --owner-ids 445189663936 --query 'Snapshots[*].{ID:SnapshotId,Desc:Description}' --output text | tr '\t' '\n' | sort) <(aws ec2 describe-volumes --query 'Volumes[*].SnapshotId' --output text | tr '\t' '\n' | sort | uniq)