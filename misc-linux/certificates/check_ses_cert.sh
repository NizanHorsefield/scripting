#!/bin/bash
working_dir=/home/oracle/smtp-cert
#set JKS_HOME
#JKS_HOME=/opt/nextees/middleware/wlserver_10.3/server/lib
JKS_HOME=/home/oracle/smtp-cert
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
		echo $NOW > $logfile
		download_cert
		del_cur_alias
		import_cert
		echo "Finished" >> $logfile
		touch $working_dir/done.txt
	fi
}

#script to download cert from AWS SES amin customer endpoint and import into demotrust
download_cert() {
	echo "Downloading" >> $logfile
	echo | openssl s_client -connect email-smtp.eu-west-1.amazonaws.com:443 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > $working_dir/cert.pem
}

#backup the current keystore
#delete current alias from the keystore
del_cur_alias() {
	echo "Deleting current" >> $logfile
	cd $JKS_HOME
	cp DemoTrust.jks "DemoTrust.jks.$NOW"
	keytool -delete -alias amazonaws -keystore DemoTrust.jks -deststorepass DemoTrustKeyStorePassPhrase
}

#import new certificate into the keystore
import_cert() {
	echo "Importing cert" >> $logfile
	cd $JKS_HOME
	keytool -import -noprompt -trustcacerts -alias amazonaws -file $working_dir/cert.pem -keystore DemoTrust.jks -deststorepass DemoTrustKeyStorePassPhrase
}

#Initial function
if [ -f $working_dir/done.txt ]
then 
	echo $NOW >> $logfile
	echo "Nothing to do" >> $logfile
else 
	check_ses_cert
fi


