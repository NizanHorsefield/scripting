#!/bin/bash
KEYTOOL_HOME=/opt/nextees/Hotspot/bin
working_dir=/home/oracle/ssl_cert_work/ADFS
#set JKS_HOME
#JKS_HOME=/opt/nextees/middleware/wlserver_10.3/server/lib
JKS_HOME=/home/oracle/ssl_cert_work/ADFS
#set keystore
#JDK
keystore=cacerts
password=changeit
#WLS
#keystore=$keystore
#password=DemoTrustKeyStorePassPhrase
#set curdate
NOW=$(date +"%m-%d-%Y")
#set up log file
logfile=$working_dir/adfs_cert.log

cd $working_dir
Cp cacerts cacerts.$NOW

certlist="RootCA-napoxfpkip001 SubCA-napdaypkip021 SubCA-napoxfpkip021"

for i in $certlist
do
        echo "importing $i"
        $KEYTOOL_HOME/keytool -import -noprompt -trustcacerts -alias $i -file $working_dir/$i-160106-DER.cer -keystore $keystore -deststorepass $password
done
echo "done"