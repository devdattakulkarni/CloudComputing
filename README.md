Code examples for Cloud Computing course
-----------------------------------------

This repository contains samples and examples demonstrating cloud resource provisioning and usage
for Amazon AWS and Google Cloud Platform (GCP).

Steps
------

1) Create virtual environment
   $ virtualenv venv
   $ source venv/bin/activate

2) Install requirements in the virtual environment
   $ pip install -r requirements.txt

3) Do AWS setup as outlined below

4) Try examples as shown below


AWS setup
-----------

1) Sign up for AWS

2) Add AWS IAM user
   Login to AWS Dashboard -> My Security Credentials -> Continue to Security Credentials -> Users -> Add User

3) Add permission to the user created
   Select user -> Add permissions -> Attach existing policies directly -> Search for "AmazonEC2FullAccess"


Examples
---------
1) VM: 
   - Examples demonstrating provisioning and management of Cloud VMs
   - Try:
     $ python VM/ec2_handler.py







