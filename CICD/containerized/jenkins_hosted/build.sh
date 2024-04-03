#!/bin/bash -x
echo "This is build step"
cd CICD
op=`helm lint wp-chart`
if [[ $op =~ "WARNING" ]]; then
   echo "FAILED"
else
   echo "SUCCESS"
fi

