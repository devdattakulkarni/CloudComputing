Code examples for Cloud Computing course
-----------------------------------------

This repository contains samples and examples demonstrating cloud resource provisioning and usage
for Amazon AWS and Google Cloud Platform (GCP).

Steps
------

1) Create virtual environment

   $ python3 -m venv venv 

   $ source venv/bin/activate

2) Install requirements in the virtual environment

   $ pip install -r requirements.txt

3) Setup PYTHONPATH

   $ export PYTHONPATH=.:$PYTHONPATH

4) Do AWS setup as outlined below

Next, you will need to setup AWS CLI on your machine.
You can do that using either the AWS setup or the Vagrant setup.


AWS setup
-----------

1) Sign up for AWS

2) Add AWS IAM user:
   Go to IAM (Search in search box on the top) ->
   Users -> Add User -> Select Access Key - Programmatic access for credential type
   
   For permission boundary, select Create user without a permissions
   boundary. Then click next to create a user.
   
   After user is created, add permission : Select user -> Add
   permissions -> Attach existing policies directly -> Search for
   "AmazonS3FullAccess"

3) Create Access Key for the User and download it as CSV to your machine.

4) Install AWS CLI and then set it up:
   - https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html
   - https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html#getting-started-quickstart-new-command
   Use the ```aws configure``` command to configure the CLI.
   
   You will be asked to enter aws_access_key_id, aws_secret_access_key, region, and output format.
   You can find names of AWS regions at the following link:

   https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html


Vagrant setup
-------------
A Vagrantfile is provided to help with the setup of a development environment with all the required tools.
It defines a Ubuntu VM and the tools that will be installed on it.
Following tools will be installed as part of VM creation: aws cli, docker, google cloud cli, helm, kubectl, minikube
Follow the below steps to get your Vagrant VM running.

1) Install Vagrant:
   - https://developer.hashicorp.com/vagrant/docs/installation

2) Install VirtualBox:
   - https://www.virtualbox.org/wiki/Downloads

3) vagrant box add bento/ubuntu-18.04

4) vagrant up

5) vagrant ssh

Once you login to the VM:
- Check /vagrant directory.
  it will be the directory on your host machine where you have the Vagrantfile 
  - Any files that you want to copy from your host machine to the VM, place them in the directory where you have the Vagrantfile and access them from /vagrant path inside your VM.
  - Any work that you do inside the /vagrant directory from inside the VM, it will be available from your host machine as well.

- Check the tools have been installed properly. 
  - aws --version
  - docker --version
  - gcloud --version
  - kubectl version
  - minikube version
  - helm version



Examples
---------
1) VM: 
   - Examples demonstrating provisioning and management of Cloud VMs
   - Try:

     $ python VM/ec2_handler.py

2) libvirt:
   - Examples demonstrating managing guest OSes (domains) on a host using libvirt
   - Try on EC2 Ubuntu 16.04 t2.micro instance

     $ sudo apt install python-pip
     $ pip install libvirt-python
     $ python libvirt/domain_handler.py

3) ObjectStores:
   - Examples demonstrating use of Cloud Object Stores (e.g. AWS S3)
   - Grant AmazonS3FullAccess permission to your IAM Service Account / User
   - Try:

     $ python ObjectStores/s3_handler.py

4) DynamoDB:
   - Starter code for working with AWS DynamoDB
   - Grant AmazonDynamoDBFullAccess to your IAM Service Account / User
