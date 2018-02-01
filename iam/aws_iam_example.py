import boto3
import logging
import os
import requests

from os.path import expanduser

home_dir = expanduser("~")

LOG_FILE_NAME = 'output.log'

AMI_NAME="ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-2018"
ROLENAME = "DescribeImagesRole"

# DescribeImagesRole policy
#    {
#      "Version": "2012-10-17",
#      "Statement": [
#          {
#              "Effect": "Allow",
#              "Action": "ec2:Describe*",
#              "Resource": "*"
#          }
#      ]
#    }

class EC2ResourceHandler:
    """EC2 Resource handler."""

    def __init__(self):

        self.client = ''

        # When running on EC2 Instance
        if not os.path.exists(home_dir + "/.aws"):
            role_url = 'http://169.254.169.254/latest/meta-data/iam/security-credentials/' + ROLENAME
            role_creds = requests.get(role_url)
            role_creds_json = role_creds.json()
            access_key_id = role_creds_json['AccessKeyId']
            secret_access_key = role_creds_json['SecretAccessKey']
            session_token = role_creds_json['Token']

            self.client = boto3.client('ec2',
                                       region_name='us-west-2',
                                       aws_access_key_id=access_key_id,
                                       aws_secret_access_key=secret_access_key,
                                       aws_session_token=session_token
                                       )
        else:
            self.client = boto3.client('ec2')

        logging.basicConfig(filename=LOG_FILE_NAME,
                            level=logging.DEBUG, filemode='w',
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        self.logger = logging.getLogger("EC2ResourceHandler")

    def _get_ami_id(self):
        self.logger.info("Retrieving AMI id")
        images_response = self.client.describe_images(
            Filters=[{'Name': 'architecture',
                      'Values': ['x86_64']},
                     {'Name': 'hypervisor',
                      'Values': ['xen']},
                     {'Name': 'virtualization-type',
                      'Values': ['hvm']},
                     {'Name': 'image-type',
                      'Values': ['machine']},
                     {'Name': 'root-device-type',
                      'Values': ['ebs']}
                     ],
        )
        ami_id = ''
        images = images_response['Images']
        for image in images:
            if 'Name' in image:
                image_name = image['Name']
                if image_name.find(AMI_NAME) >= 0:
                    ami_id = image['ImageId']
                    break
        return ami_id
    
    def describe_images(self):
        ami_id = self._get_ami_id()        
        print("AMI ID: %s" % ami_id)

    def run_instances(self):
        response = self.client.run_instances(
            ImageId='ami-a9d736c9',
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            Monitoring={'Enabled': False},
        )

def main():
    ec2_handler = EC2ResourceHandler()
    
    # 1) Invoking a call that is allowed by the Role ROLENAME
    print("Finding AMI ID for %s" % AMI_NAME)
    instance_id = ec2_handler.describe_images()

    # 2) Invoking a call that is not allowed by the Role ROLENAME
    # print("Invoking run_instances()")
    # ec2_handler.run_instances()

if __name__ == '__main__':
    main()