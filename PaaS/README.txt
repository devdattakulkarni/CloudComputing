AWS-Beanstalk
--------------
This directory contains Python based sample web application.
Use this application as a starting point for your code.

Follow the README inside this directory to deploy this application
on AWS Elastic Beanstalk


FirstMile
----------
This directory contains steps to install and use the FirstMile cloud developer sandbox

https://github.com/cloud-ark/firstmile.

You can use FirstMile when you are developing your web application locally.
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

