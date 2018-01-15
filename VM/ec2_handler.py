import ast
import boto3
import logging
import os

from common import common_functions

LOG_FILE_NAME = 'output.log'

class EC2ResourceHandler:
    """EC2 Resource handler."""

    def __init__(self):
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
                # This image is available for free tier
                if image_name.find("ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-2018") >= 0:
                    ami_id = image['ImageId']
                    break
        return ami_id

    def create(self, name='', flavor=''):
        self.logger.info("Name:%s Flavor:%s" % (name, flavor))

        ami_id = self._get_ami_id()

        response = self.client.run_instances(
            ImageId=ami_id,
            InstanceType='t2.micro',
            MaxCount=1,
            MinCount=1,
            Monitoring={'Enabled': False},            
        )
        return

    def get(self):
        self.logger.info("Entered get")
        # Add logic to get information about the created instance
        # Use describe_instances call

        # Add code to return from get only after the instance state becomes 'running'
        
        return

    def delete(self):
        self.logger.info("Entered delete")

        # Add logic to terminate the created instance
        # Use terminate_instances call

        # Should return from the call only after the instance has been terminated (i.e.
        # the instance is not available using the 'get' call

        return


def main():
    
    available_cloud_setup = common_functions.get_cloud_setup()
    if 'aws' not in available_cloud_setup:
        print("Cloud setup not found for aws.")
        print("Doing the setup now..")
        os.system("pip install awscli")
        os.system("aws configure")

    ec2_handler = EC2ResourceHandler()

    print("Spinning up EC2 instance")
    ec2_handler.create(name='test', flavor='test')
    print("EC2 instance provisioning started")

    ec2_handler.get()

    ec2_handler.delete()


if __name__ == '__main__':
    main()