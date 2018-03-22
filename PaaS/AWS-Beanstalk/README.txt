1) Give AWSElasticBeanstalkFullAccess managed policy permission to your IAM User

2) Add following Inline policy:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticbeanstalk:*",
                "ec2:*",
                "elasticloadbalancing:*",
                "autoscaling:*",
                "cloudwatch:*",
                "s3:*",
                "sns:*"
            ],
            "Resource": "*"
        }
    ]
}

3) Check steps.txt inside greetings folder

4) Follow similar steps to deploy greetings application in your account

5) Point the browser to the CNAME of the environment


