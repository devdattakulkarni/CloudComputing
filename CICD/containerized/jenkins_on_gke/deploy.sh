#!/bin/bash -x
echo "This is deploy step"
ls
kubectl get pods
helm upgrade --install wordpress wp-chart -n default
kubectl get pods

