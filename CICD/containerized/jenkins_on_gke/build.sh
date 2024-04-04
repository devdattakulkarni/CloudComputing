#!/bin/bash -x
echo "This is build step"
op=`helm lint wp-chart`
if [[ $op =~ "WARNING" ]]; then
   echo "FAILED"
else
   echo "SUCCESS"
fi

