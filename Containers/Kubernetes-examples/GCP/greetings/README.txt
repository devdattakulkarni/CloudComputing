Greetings
----------

This example shows deployment of a web application that uses MySQL backend.

Several environment definition files are available:

1) environment-local.yaml: Environment definition containing MySQL container platform element
2) environment-rds-local.yaml: Environment definition containing RDS resource. The RDS instance
   is open so as to allow connecting application container running locally on your machine
3) environment-rds-ecs.yaml: Environment definition containing RDS and ECS cluster resource.
4) environment-cloudsql-gke.yaml: Environment definition containing Cloud SQL and GKE cluster resource. 

Several application definition files are available:

1) app-local.yaml: Application definition for local deployment of application
2) app-aws.yaml: Application definition for AWS ECS deployment
3) app-gcloud.yaml: Application definition for Google GKE deployment
4) greetings-pod.yaml: Kubernetes Pod definition for Google GKE deployment 



===============
Deploy Locally
===============

Deploy application locally binding to local MySQL container

$ cld env create env-local environment-local.yaml

$ cld container create cont1 local

Edit app-local.yaml to include image id obtained from output of command:

$ cld container show cont1

$ cld app deploy greetings-local env-local app-local.yaml


==================
Deploy on AWS ECS
==================

Deploy application on ECS binding to a RDS instance

$ cld env create env-aws environment-rds-ecs.yaml

$ cld container create cont2 ecr

Edit app-aws.yaml to include image url obtained from output of command:

$ cld container show cont2

$ cld app deploy greetings-aws env-aws app-aws.yaml


======================================
Deploy on Google GKE - using app yaml
======================================

Deploy application on GKE binding to a Cloud SQL instance

$ cld env create env-gcloud environment-cloudsql-gke.yaml

$ cld container create cont3 gcr

Edit app-gcloud.yaml to include image url obtained from output of command:

$ cld container show cont3

$ cld app deploy greetings-gke env-gcloud app-gcloud.yaml


======================================
Deploy on Google GKE - using Pod yaml
======================================

Deploy application on GKE binding to a Cloud SQL instance

$ cld env create env-gcloud environment-cloudsql-gke.yaml

$ cld container create cont3 gcr

Edit greetings-pod.yaml to include image url obtained from output of command:

$ cld container show cont3

$ cld app deploy greetings-gke env-gcloud greetings-pod.yaml


Track / Debug:
---------------

$ cld env show <env-name>

$ cld app show <app-name>

$ cld app logs <app-name>

$ cld env shell <env-name>


Verify:
-------

$ cld app show <app-name>

$ cld app list

$ cld env show <env-name>

$ cld env list


Cleanup:
--------

$ cld app delete <app-name>

$ cld env delete <env-name>

$ cld container delete <container-name>
