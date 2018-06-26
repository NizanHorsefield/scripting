#!/bin/bash

for D in */;
do
  echo $D
  cd $D
  git remote  -v    
  cd ..
done
