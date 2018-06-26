#!/bin/bash

#  NDH
# 19th Jan 2018
# The script creates images from running nonprod DB instances
# AWS keys must be setup seperately, preferably using an EC2 that has an IAM Role

export EC2_HOME=/usr/local/ec2-api-tools-1.6.1.3
export EC2_BIN=$EC2_HOME/bin
export PATH=${PATH}:${EC2_BIN}:/usr/local/s3cmd-1.1.0-beta3/:/usr/local/ec2-api-tools-1.6.1.3/bin/:/usr/local/ec2/bin/
export JAVA_HOME=/usr/java/jdk1.7.0_09
export EC2_URL=https://ec2.eu-west-1.amazonaws.com

mkdir -p /tmp/audit 
audit_log="/tmp/audit/audit_history_created_on_`date +%F`_np.log"
(
    #set the s3 bucket name and folder that could content the log file
    s3_bucketname="image-backup-store/image-backup-log"
    echo "S3 bucket/folder details were log file will be stored: $s3_bucketname"

    todayDate=`date +%F`

    mkdir -p /tmp/backup

    #To store the instances backup details in a log file is set in a temp variable
    log_filename="image_backedup_on_"$todayDate"_np.csv"
    log_file="/tmp/backup/$log_filename"
    echo "Instances and AMI details are stored into log file  $log_file temporary before moving to S3 location"

    if [[ -f $log_file ]]
    then
        echo "log file $log_file already exists, it will be deleted for taking backup details"
        rm -rf $log_file
        if [[ $? == 0 ]]
        then
            echo "log file $log_file deleted successfully"
        fi
    fi

    #Set the environment to be used
    #envi=$1
    envi="CERT,SIT2,SIT1,DEV,DEV2"

    #Set the  file that will be used to output the results of AWS command
    ec2InfoFile="/tmp/backup/ec2_list"

    #list all the instances based on the filter and write to $ec2InfoFile
    #ec2Info=`aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" "Name=tag:Name, Values=evise-db-cert" > $ec2InfoFile`
    #ec2Info=`aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" "Name=tag:Name, Values=evise-db-sit2" >> $ec2InfoFile`
    #ec2Info=`aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" "Name=tag:Name, Values=evise-db-sit1" >> $ec2InfoFile`
    #ec2Info=`aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" "Name=tag:Name, Values=evise-db-dev2" >> $ec2InfoFile`
    #ec2Info=`aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" "Name=tag:Name, Values=evise-db-dev1" >> $ec2InfoFile`

    instances=($(cat $ec2InfoFile | grep "evise-db" |  awk '{print $1}' | sort -u))
    numOfInstances=`cat $ec2InfoFile | grep "evise-db" |  awk '{print $1}' | sort -u | wc -l`
    read -p "DEBUG 1"
    echo "No of $envi instances are : $numOfInstances"

    #Calculate lenght of instance array
    arraylength="${#instances[@]}"

    echo "No of Instances in Array is : $arraylength"

    #setting header in log file
    echo "#BACKUP LOG DETAILS FOR $todayDate Date"	> $log_file
    echo "#Sl No,Instance ID,AMI ID,Instance Name,AMI Name" >> $log_file

    echo "The instance IDs are as follows follows ..."
    read -p "DEBUG 2"
    #Create images for all instances identified
    for (( i=0; i<${arraylength}; i++ ));
     do
        sl_no=`expr $i + 1`
    
        iName=`cat $ec2InfoFile | grep "evise-db" | grep -i "${instances[i]}" | awk '{print $2}'`
        ami_name=$iName"-"$todayDate
        ami_description=`echo 'BackupImage for instance '$iName' with instanceID' ${instances[i]} ' created on ' $todayDate`

        echo "------------------------------------------------------------------------------------"
        echo "Sl. No : "$sl_no
        echo "AMI will be created for ... "
        echo "        Instance Name: " $iName
        echo "        Instance ID:" ${instances[i]}
        echo "with following details"
        echo "        AMI Name: " $ami_name
        echo "        AMI Description: " $ami_description

        ami_id="`ec2 create-image ${instances[i]} --name $ami_name --description $ami_description --no-reboot | awk '{print $2}'`"
        echo "ec2 create-image ${instances[i]} --name $ami_name --description $ami_description --no-reboot | awk '{print $2}'"
        if [[ $? -eq 0 ]]
        then
            echo "AMI ID Created is:" $ami_id
        elif [[ $? -gt 0 ]]
        then
            echo "AMI ID Creation failed"
        fi
        echo "$sl_no,${instances[i]},$ami_id,$iName,$ami_name" >> $log_file
     done
    read -p "DEBUG 3"
    #Move log file to s3 bucket
    s3cmd --config /root/.s3cfg put $log_file s3://$s3_bucketname/ 1>/tmp/output.tmp
    val_cnt=$?
    if [[ $val_cnt -eq 0 ]]
    then
        echo "log file $log_filename uploaded successfully into S3 bucket at $s3_bucketname"
    elif [[ $val_cnt -gt 0 ]]
    then
        echo "Upload failed for $log_filename file into S3 bucket at $s3_bucketname"
    fi
    #/bin/rm -rf /tmp/output.tmp $ec2InfoFile
) > $audit_log
read -p "DEBUG 4"
#this is outside the audit log block
s3_bucketname="image-backup-store/image-backup-log"

if [[ -f $audit_log ]]
then
s3cmd --config /root/.s3cfg put $audit_log s3://$s3_bucketname/ 1>/tmp/output.tmp
val_cnt=$?
	if [[ $val_cnt -eq 0 ]]
	then
        	echo "audit log file $audit_log uploaded successfully into S3 bucket at $s3_bucketname"
	elif [[ $val_cnt -gt 0 ]]
	then
        	echo "Upload failed for $audit_log file into S3 bucket at $s3_bucketname"
		echo "File is present locally as $audit_log"
	fi
fi
read -p "DEBUG 5"
/bin/rm -rf /tmp/output.tmp
