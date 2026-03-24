Commands to test:
------------------

Create s3 bucket with the name <BUCKET_NAME>.
You can use aws cli or web console for this step.

Login to your AWS account through the web console and create a SSK key pair named "assignment4". 
Download the .pem file (assignment4.pem) on your machine. 
This SSH key pair will help you to login to the created VM. 
The public key will be injected into the VM, and the private key will be 
available on your machine (this is the .pem file).


1) Copy files to s3 bucket:
aws s3 cp application.py s3://<BUCKET_NAME>/application.py
aws s3 cp requirements.txt s3://<BUCKET_NAME>/requirements.txt

2) Create CF stack:
aws cloudformation create-stack \
  --stack-name assignment4 \
  --template-body file://cf_template.yaml \
  --parameters \
    ParameterKey=KeyName,ParameterValue=assignment4 \
    ParameterKey=S3BucketName,ParameterValue=<BUCKET_NAME> \
    ParameterKey=EnvValue,ParameterValue="Testing CloudFormation" \
  --capabilities CAPABILITY_NAMED_IAM

3) Wait for stack creation:
aws cloudformation wait stack-create-complete \
  --stack-name assignment4

4) Get Public IP address:
aws cloudformation describe-stacks \
  --stack-name assignment4 \
  --query "Stacks[0].Outputs[?OutputKey=='PublicIP'].OutputValue" \
  --output text

5) Verify:
curl http://<PUBLIC_IP>

6) Delete stack;
aws cloudformation delete-stack \
  --stack-name assignment4

7) Ssh into the VM:
ssh -i assignment4.pem ubuntu@<PUBLIC_IP>

8) Check logs:
cat /var/log/cloud-init-output.log
cat /home/ubuntu/app/app.log

