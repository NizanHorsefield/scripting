#!/bin/bash
while IFS=$',' read -r -a myArray
do
 echo "${myArray[0]}"
 echo "${myArray[1]}"
 echo "${myArray[2]}"
done <  managed_servers.local_docker

OIFS=$IFS;
IFS=",";

servers=`cat managed_servers.local_docker`
serversArray=$servers;

for server in $serversArray
do
    echo $server
done

IFS=$OIFS;