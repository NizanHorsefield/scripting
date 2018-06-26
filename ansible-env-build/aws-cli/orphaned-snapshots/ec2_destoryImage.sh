#!/bin/bash
set -x

# Created On 	: 2014-05-05
# author & Company : Wipro Technolgies Ltd
#
# ScriptName	: ec2_destroy_image.sh
# Description 	: To delete the images passed through log file as parameter. The script takes two paramater 1.log file name from S3 bucket and 
#		2. buket name with folder name. Taking this as input the script deletes the ami images and creates a new log file with all
#		the deleted images with their AMI ID and Instance ID details.
# Usage of Script:
#
#		./ec2_destory_image.sh -f image_backedup_on-2014-05-05.csv -b image-backup-store/image-backup-log
#
# Output of script:
#
#	Creates a log file by name image-destroyed-<YYYY>-<MM>-<DD> locally.
#	Moves the locally created file into S3 bucket at path image-backup-store/image-deleted-log/


usage()
{
echo "Usage of script: ./ec2_destory_image.sh -f <log-file-name> -b <s3-bucket-name>/<folder-name-if-any>"
echo "For Ex: ./ec2_destory_image.sh -f image_backedup_on-2014-05-05.csv -b image-backup-store/image-backup-log"
exit 1
}


while getopts ":f:b:" case_value; do
    case "${case_value}" in
        f)
            log_filename=${OPTARG}
            ;;
        b)
            bucket_path=${OPTARG}
            ;;
        *)
            echo "INVALID PARAMETER SPECIFIED"
	    usage
            ;;
    esac
done

if [[ -z "$log_filename" || -z "$bucket_path" ]]
then
	usage
fi


#set S3 bucket details for uploading of log file
s3bucket_det="image-backup-store/image-deleted-log/"

#get the date from the entered log file as parameter:
backedup_date=`echo $log_filename | awk -F'_' '{print $NF}' | awk -F'.' '{print $1}'`

#set today's date
todayDate=`date +%F-%H-%M-%S`
echo "Today's Date $todayDate"


mkdir -p /tmp/delete_bucket
mkdir -p /backupInfo/ami2bedeleted/
#set log file path and name
del_filename="image_destroyed_on_${todayDate}_for_${backedup_date}.csv"
echo "Log file name created with name $del_filename"

log_file="/backupInfo/ami2bedeleted/$del_filename"

if [[ -f $log_file ]]
then
	echo "Log file provided is already exists at $log_file, remove the file to proceed"
	exit 1
fi

/bin/rm -rf /backupInfo/ami2bedeleted/$log_filename
purge_ami="N"
#pull the log file from bucket
s3cmd get s3://$bucket_path/$log_filename /backupInfo/ami2bedeleted/$log_filename 1>/backupInfo/ami2bedeleted/get_loglist_${todayDate}.log
if [[ $? -eq 0 ]]
then
	echo "log file $log_filename is downloaded locally"
#	echo "Are You Sure to delete the AMI Image[Y/N]?"
#	read ans
#	if [[ $ans == "Y" || $ans == "y" ]]
#	then
		purge_ami="Y"
#	fi
elif [[ $? -gt 0 ]]
then
	echo "Please check for the log file name or the file is locally present in /backupInfo/ami2bedeleted/ directory"
fi


if [[ "$purge_ami" == "Y" ]]
then

#temp file for storing snapshots
snapshot_logfile="snapshot_details_${todayDate}.log"
snapshot_log="/backupInfo/ami2bedeleted/$snapshot_logfile"
ec2-describe-snapshots > $snapshot_log

#Creates header for deleted image log file
echo "#Listed of AMI's Created on $backedup_date are deleted on $todayDate" > $log_file
echo "#SL.No,AMI ID,AMI Name,Instance ID,Instance Name,Snapshot ID,Deleted[Y/N]" >> $log_file

#parse through the provided log file and fetch only the uncommented code for processing
/bin/cat /backupInfo/ami2bedeleted/$log_filename | grep -v "#" > /backupInfo/ami2bedeleted/ami_inst_det_${todayDate}.tmp	

#Set the total number of ami's to be deleted
ami_cnt=`/bin/cat /backupInfo/ami2bedeleted/ami_inst_det_${todayDate}.tmp | wc -l`
echo "Total No of AMI's to be Deleted:" $ami_cnt

sl_cnt=1

for file_line in `cat /backupInfo/ami2bedeleted/ami_inst_det_${todayDate}.tmp`
do
	echo "-----------------------------------------"
	sl_no=`echo $file_line | awk -F',' '{print $1}'`
	echo "Sl No" $sl_no
	ami_id=`echo $file_line | awk -F',' '{print $3}'`
	echo "AMI ID" $ami_id
	inst_id=`echo $file_line | awk -F',' '{print $2}'`
	echo "Instance Id" $inst_id
	inst_name=`echo $file_line | awk -F',' '{print $4}'`
	echo "Instance Name" $inst_name
	ami_name=`echo $file_line | awk -F',' '{print $5}'`
	echo "AMI Name" $ami_name
	echo "Deleting the Image with ID : " $ami_id
	deleted_amiid="`ec2-deregister $ami_id | awk '{print $2}'`"
#	deleted_amiid=$ami_id
	if [[ $? -eq 0 && -n "$ami_id" && "$ami_id" == "$deleted_amiid" && -n "$deleted_amiid" ]]
	then
		echo "Image with AMI ID $ami_id Deleted Successfully"
		del_flag="Y"
	else
		echo "Image with AMI ID $ami_id did not get Deleted"
		del_flag="N"
	fi
	#code to delete the snapshots for the deleted AMI
	if [[ $del_flag == "Y" || $del_flag == "y" ]]
	then
		echo "Deleting below snapshot ID's related to AMI $deleted_amiid at $(date +%F-%H-%M-%S)" 

		snapshot_det=($(sed -n '/'$deleted_amiid'/p' $snapshot_log | awk '{print $2}'))
		snaphost_arrlen="${#snapshot_det[@]}"
		for (( i=0;i<$snaphost_arrlen;i++ ));
		do
			deleted_snapId="`ec2-delete-snapshot ${snapshot_det[i]} | awk '{print $2}'`"
			echo "Deleted snapshot ID $deleted_snapId"
                        echo "$sl_cnt,$ami_id,$ami_name,$inst_id,$inst_name,${snapshot_det[i]} ,$del_flag" >> $log_file

		done
	fi
	echo "$sl_cnt,$ami_id,$ami_name,$inst_id,$inst_name,$del_flag" >> $log_file
	echo "Details for AMI ID $ami_id is saved in log file"
	sl_cnt=`expr $sl_cnt + 1`
	sleep 1 
done


#upload the log file into S3 bucket
s3cmd put $log_file s3://$s3bucket_det 1>/backupInfo/ami2bedeleted/del_output_${todayDate}.tmp
val_cnt=$?
	if [[ $val_cnt -eq 0 ]]
	then
        	echo "log file $log_filename uploaded successfully into S3 bucket at $s3_bucketname"
	elif [[ $val_cnt -gt 0 ]]
	then
        	echo "Upload failed for $log_filename file into S3 bucket at $s3_bucketname"
	fi
fi


#delete the all the temporary files and log files from local machine
#/bin/rm -rf /backupInfo/ami2bedeleted/ami_inst_det_${todayDate}.tmp /backupInfo/ami2bedeleted/del_output_${todayDate}.tmp /backupInfo/ami2bedeleted/get_loglist_${todayDate}.log /tmp/$log_filename $snapshot_log 
	echo "Deteled all the temporary files and log file generated from local machine"
	echo "END OF SCRIPT"
