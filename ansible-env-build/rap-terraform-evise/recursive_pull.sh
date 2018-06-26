#!/bin/bash

for D in */;
do
  echo $D
  cd $D
  git pull    
  cd ..
done
