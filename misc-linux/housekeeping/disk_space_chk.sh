#!/bin/sh
xemails="nizan.horsefield@gmail.com,nizan.horsefield@reedelsevier.com,r.marsh@elsevier.com,R.Karelia@elsevier.com,G.Mahadevan@elsevier.com,m.deshpande@elsevier.com,e.biegel@elsevier.com,sabyasachi.malakar@wipro.com"
df -H | grep -vE '^Filesystem|tmpfs|cdrom' | awk '{ print $5 " " $1 }' | while read output;
do
  echo $output
  usep=$(echo $output | awk '{ print $1}' | cut -d'%' -f1  )
  partition=$(echo $output | awk '{ print $2 }' )
  echo $usep
  if [ $usep -ge 90 ]; then
    echo "Running out of space \"$partition ($usep%)\" on $(hostname) as on $(date)" |
     mail -s "Alert: Disk space usage is  $usep%" $xemails
  fi
done
