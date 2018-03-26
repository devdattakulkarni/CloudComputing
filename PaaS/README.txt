AWS-Beanstalk
--------------
This directory contains Python based sample web application.
Use this application as a starting point for your code.

Follow the README inside this directory to deploy this application
on AWS Elastic Beanstalk


FirstMile
----------
FirstMile is a command-line tool that simplifies development and deployment of
web applications for Amazon Elastic Beanstalk and Google App Engine.

https://github.com/cloud-ark/firstmile.

In the FirstMile directory you will find two files:
1) steps-to-deploy-app-service-separately.txt

   This file shows how FirstMile can be used to provision a MySQL service instance
   first and then bind it to a web application locally.

   Using this approach you can provision a MySQL instance once and then bind that
   instance when an app is deployed subsequently. Each app deployment will create
   a new version of the app available on different URLs. Each of these deployments
   will bind to the same MySQL service instance.

2) steps-to-deploy-app-service-together.txt

   This file shows how FirstMile can be used to deploy a web application along with
   a MySQL service instance as a single step.

   A new MySQL service instance is created for each application deployment in this approach.

   This is useful when you want to use a fresh MySQL instance with a deployed application.

Once you are ready you can use FirstMile to also deploy the application to Elastic Beanstalk.

FirstMile has been tested on Ubuntu 14.04/16.04 and Mac OS X (El Capitan).
If you don't have one of these machines you can create a AWS Ubuntu VM and
install FirstMile on it. Apply following security group to your instance.

Name: DockerPorts
Description: DockerPorts
Protocol: TCP
Port range: 32700 - 32800
CIDR Address: 0.0.0.0/0, ::/0

After this security group is applied, you will be able to open your locally deployed
application at a URL of following form:

http://<VM-Public-IP>/<port>

The <port> is output of following command:

$ cld app show --deploy-id <dep-id>


-----------------------------------

How does FirstMile work?
------------------------
FirstMile uses Docker to package your application and deploy it. 
For MySQL service, FirstMile deploys a MySQL Docker container.


How is FirstMile different from docker-compose?
-----------------------------------------------
For local development use-case FirstMile and docker-compose are kind of similar. 

Where FirstMile is different is that, besides local development, it also allows you to deploy same code, without any
modifications, to AWS Beanstalk and Google App Engine. This is not possible with docker-compose.
