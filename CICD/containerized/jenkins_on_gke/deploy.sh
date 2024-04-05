#!/bin/bash -x
echo "This is deploy step"
ls
kubectl get pods -A
helm upgrade --install wordpress wp-chart -n default
kubectl get pods -A

