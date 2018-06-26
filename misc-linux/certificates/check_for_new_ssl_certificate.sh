#!/bin/bash
working_dir=/home/nizanh
#set curdate
NOW=$(date +"%m-%d-%Y")
#set up log file
logfile=$working_dir/aws_ses.log

#check expiration of current AWS SES CERTIFICATE
check_ses_cert() {
	check=`echo | openssl s_client -connect email-smtp.eu-west-1.amazonaws.com:443 2>/dev/null | openssl x509 -noout -dates | grep 'Oct 10' | awk -F'=' '{print $2}'`
	if [[ $check == "Oct 10 23:59:59 2015 GMT" ]]
	then
		echo "CERT expires on Oct 10";
	else
		echo "I've found a new certificate on the AWS SES main end point at $(date)" | mail -s "AWS SES CERTICATE CHANGE FOUND - CHECK OSB" nizan.horsefield@gmail.com
		touch $working_dir/done.txt 
	fi
}

#Initial function
if [ -f $working_dir/done.txt ]
then 
	echo $NOW >> $logfile
	echo "Nothing to do" >> $logfile
else 
	check_ses_cert
fi