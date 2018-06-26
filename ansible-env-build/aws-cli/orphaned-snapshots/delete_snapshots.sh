#!/bin/bash


del_no_ami_snapshots(){
    while read s ;
    do
      echo "aws ec2 delete-snapshot --region eu-west-1 --snapshot-id $s"
      aws ec2 delete-snapshot --region eu-west-1 --snapshot-id $s
    done < no_ami.list
}

del_fully_orphaned_snapshots(){
    while read s ;
    do
      echo "aws ec2 delete-snapshot --region eu-west-1 --snapshot-id $s"
      aws ec2 delete-snapshot --region eu-west-1 --snapshot-id $s
    done < fully_orphaned.list
}

del_no_instance_snapshots(){
    while read s ;
    do
      echo "aws ec2 delete-snapshot --region eu-west-1 --snapshot-id $s"
      aws ec2 delete-snapshot --region eu-west-1 --snapshot-id $s
    done < no_instance.list
}

del_no_ami_snapshots