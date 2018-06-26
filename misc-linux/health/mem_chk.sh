#!/bin/sh
#xemails="nizan.horsefield@gmail.com,nizan.horsefield@reedelsevier.com,r.marsh@elsevier.com,R.Karelia@elsevier.com,G.Mahadevan@elsevier.com,m.deshpande@elsevier.com,e.biegel@elsevier.com,sabyasachi.malakar@wipro.com"

xemails="nizan.horsefield@reedelsevier.com"

FREE_DATA=`free -m | grep Mem` 
CURRENT=`echo $FREE_DATA | cut -f3 -d' '`
TOTAL=`echo $FREE_DATA | cut -f2 -d' '`
RAM=$(echo "scale = 2; $CURRENT/$TOTAL*100" | bc)
COMP=`echo $RAM | nawk '{printf("%d\n", $1 * 10)}`
if [ $COMP -ge 10 ]; then
   echo "Running out of systme memory on $(hostname) as on $(date)" |
   mail -s "Alert: Memory usage is  $RAM%" $xemails
fi
