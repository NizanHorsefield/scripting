#!/bin/bash

#Setting things up
LOG_DIR='/tmp/'
LOG_FILE=$LOG_DIR'nc_test.log'
NOW=$(date +"%m-%d-%Y")
COUNT=0

echo $NOW >> $LOG_FILE

#Functions to check connectivity
promis_db_check(){
	DB_CHECK=`nc -z -w 5 10.58.16.53 1521 | grep succeeded`
	if [ ! -z "$DB_CHECK" -a "$DB_CHECK" != " " ]; then
			return 0
		else
			return 1
	fi
}

obiee_check(){
	OB_CHECK=`nc -z -w 5 10.58.130.19 9704 | grep succeeded`
	if [ ! -z "$OB_CHECK" -a "$OB_CHECK" != " " ]; then
			return 0
		else
			return 1
	fi
}

pts_check(){
	PTS_CHECK=`nc -z -w 5 10.58.16.103 7788 | grep succeeded`
	if [ ! -z "$PTS_CHECK" -a "$PTS_CHECK" != " " ]; then
			return 0
		else
			return 1
	fi
}

oem_check(){
	OEM_CHECK=`nc -z -w 5 10.196.188.197 4900 | grep succeeded`
	if [ ! -z "$OEM_CHECK" -a "$OEM_CHECK" != " " ]; then
			return 0
		else
			return 1
	fi
}

promis_db_check
if [ $? = '0' ]; then
	echo "Connected to PROMIS DB" >> $LOG_FILE
	COUNT=$(( $COUNT +1 ))
else
	echo "Failed to connect to Promis DB" >> $LOG_FILE
fi
obiee_check
if [ $? = '0' ]; then
	echo "Connected to OBIEE" >> $LOG_FILE
	COUNT=$(( $COUNT +1 ))
else
	echo "Failed to connect to OBIEE" >> $LOG_FILE
fi
pts_check
if [ $? = '0' ]; then
	echo "Connected to PTS" >> $LOG_FILE
	COUNT=$(( $COUNT +1 ))
else
	echo "Failed to connect to PTS" >> $LOG_FILE
fi
oem_check
if [ $? = '0' ]; then
	echo "Connected to OEM" >> $LOG_FILE
	COUNT=$(( $COUNT +1 ))
else
	echo "Failed to connect to OEM" >> $LOG_FILE
fi

if [ $COUNT = 4 ]; then
	echo "Tests Succeeded " 
else
	echo $COUNT "out of 4 test succeeded - check" $LOG_FILE
fi
























