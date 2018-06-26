#!/bin/bash
echo " start " > list_names.txt
while read -r b; do
   #echo $b
   name=$(aws ec2 describe-instances --filter Name=private-ip-address,Values=$b --query 'Reservations[].Instances[].[Tags[?Key==`Name`].Value]' --output text)
   echo $b $name >> list_names.txt
done < list