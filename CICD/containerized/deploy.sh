#!/bin/bash -x
echo "This is deploy step"
ls
export KUBECONFIG=kubeconfig.json
gcloud auth activate-service-account --key-file kubeconfig.json
gcloud config set project <insert-your-gcloud-project-name>
gcloud container clusters get-credentials <insert-your-cluster-name>  --zone=us-central1-b
helm delete wordpress -n default -v6
helm install wordpress wp-chart --kubeconfig=kubeconfig.json -n default -v6
