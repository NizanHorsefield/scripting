#!/bin/bash

# Author : Nizan Horsefield
# Date : 19th March 2018
# Version : 00.01
# JIRA : EVISEP-12106

# set
NOW=$(date +"%Y-%m-%d-%H:%M:%S")
site="http://download.nai.com/products/DatFiles/4.x/nai/"
working_dir=$(pwd)
working_name="avvepo-latest"
working_file="$working_name.zip"
final_file="avvdat-latest.zip"
s3_location="s3://evise-installation-media/McAfee"
logfile=$working_dir/av_dat_download.log
arn="arn:aws:sns:eu-west-1:445189663936:nizanhorsefieldonly"

# clean
clean_working(){
    echo "Changing to $working_dir in order to delete $final_file"
    cd $working_dir
    rm *.zip
    rm *.log
    }

init_logging(){
#write to log file
    echo "$NOW: " >> $logfile
}
# get the name of the latest av dat zip file and download it
get_datzip_byname(){
    cd $working_dir
# use curl to get the name of file to download
    list=$(curl -s "$site" --list-only | grep avvepo | awk '{print $5}' | awk '{print $1}' )
    IFS='" ' read -r -a array <<< "$list"
    echo "Latest file to be downloaded is ${array[1]}" >> $logfile
    file="${array[1]}"
    remote_file="$site/$file"

# use curl to download the file and rename
    echo "Downloading $file" >> $logfile
    curl $remote_file  --output $working_name.zip
}

# change the working directory and extract the dat zip file
extract_avdefs(){
# the zip file from macafee is for EPO so we now need to extract the dat zip from it.
    unzip -d $working_name $working_name.zip
    cp $working_name/avvdat-*.zip $final_file
}

# now copy the file up to S3
copy_to_s3() {
  if [ -f $working_dir/$final_file ]; then
       echo "Success - file $final_file exists locally, and is ready to be copied to S3." >> $logfile
       aws s3 cp $working_dir/$final_file $s3_location/$final_file
    else
       echo "File $final_file does not exist locally." >> $logfile
    fi
}

check_s3_copy(){
    check=$(aws s3 ls $s3_location/$final_file | awk '{print $4}')
    if [ "$check" == "$final_file" ]; then
       echo "Success - file $final_file has been copied to S3." >> $logfile
       rm -rf $working_dir/$working_name
       rm $working_dir/$working_file
       # send a message that everything is OK
       aws sns publish --topic-arn $arn --message "Success - file $final_file was downloaded, and has been copied to S3"
    else
       echo "File $final_file does not exist in S3." >> $logfile
       # send a message that everything something went wrong
       aws sns publish --topic-arn $arn --message "Failure - file $final_file was not downloaded, so has not been copied to S3"
    fi
}

clean_working
# read -p "Press any key to continue... " -n1 -s
init_logging
get_datzip_byname
extract_avdefs
copy_to_s3
check_s3_copy