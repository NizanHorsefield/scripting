#!/bin/sh
#set -x
#set curdate
NOW=$(date +"%Y-%m-%d-%H:%M:%S")
#NOW=$(date +"%m-%d-%Y")
#set up log file
working_dir=/home/oracle/scripts/adf_response
logfile=$working_dir/adf_resp.log
#set the external emails
xemails1="nizan.horsefield@reedelsevier.com,s.smith.1@elsevier.com,karlo.vida@reedelsevier.com,johnaudie.jaro@reedelsevier.com,d.ma@elsevier.com,c.rylett@elsevier.com"
xemails="evise-prod@elsevier.pagerduty.com"
xemails2="nizan.horsefield@gmail.com,nizan.horsefield@reedelsevier.com,s.smith.1@elsevier.com,h.nehru@elsevier.com,j.miller.1@elsevier.com,sabyasachi.malakar@wipro.com,a.hough@elsevier.com,rohit.wadhwa@wipro.com,uma.ashwhinkumar@wipro.com,ssmith@hotmail.fr,karlo.vida@reedelsevier.com,johnaudie.jaro@reedelsevier.com,m.eamens@elsevier.com"

# What to check
SCHEME="http://"
APP_URI="/evise/faces/pages/navigation/NavController.jspx"
MS_PORT="26820"

#write to log file
echo "$NOW: " >> $logfile

while read server; do
  URL=$SCHEME$server":"$MS_PORT$APP_URI
  response=$(/usr/bin/curl -o /dev/null --silent --head --write-out '%{http_code}' "$URL" | /bin/awk '{print $1}')
  
  if [ $response == '500' ]; then
    echo $URL "-" $response " - FAILURE">> $logfile
    echo "ADF Managed server \"$server\" has returned an HTTP 500 error" | mail -s "Alert - ADF Managed server \"$server\" has returned an HTTP 500 error" $xemails1
 
  elif [ $response != '500' ]; then
    echo $URL "-" $response " - OK" >> $logfile
    #touch $working_dir/alert.lck

  fi
done <  $working_dir/url-list.txt