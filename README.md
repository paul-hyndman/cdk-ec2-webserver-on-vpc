# cdk-ec2-webserver-on-vpc
Project using Python CDK to create EC2 web server on a VPC

# A demo project illustrating how to deploy an AWS EC2 web server using Python CDK.
# Project creates AWS artifacts:
#  - VPC
#  - EC2
#  - S3
# User data to launch Apache webserver with custom index.html page is loaded from S3 bucket

Requirements:
 - A command shell such as Git Bash
 - Python
 - CDK
 - Node JS/NPM for miscellaneous package installs

Modify cdk.json with your account in the "envs" configuration

To create the web server:
    1. Run pip install -r requirements.txt from root of project
    2. Modify app.py to deploy S3 buket (uncomment line "S3CreateProject(app, "S3CreateProject", env=env_dev)")
        - From project root run "cdk init" to check for errors, then "cdk deploy"
    3. From root of project copy html file to S3
        -  aws s3 cp index.html s3://<<your bucket name>>/index.html
    4. Modify app.py to deploy VPC (uncomment line "CustomVpcStack(app, "CustomVpcStack", env=env_dev)")
        - From project root run "cdk init" to check for errors, then "cdk deploy CustomVpcStack --require-approval never"
        - This can take a while to deploy
    5. Verifying deploy of VPC on AWS console
        - From AWS console you can find it via VPC->You VPCs
    6. Modify app.py to deploy EC2 (uncomment line "CustomVpcStack(app, "CustomVpcStack", env=env_dev)"
        - Modify class CustomEc2Stack to use ID of VPC created in step #4
        - From project root run "cdk init" to check for errors, then "cdk deploy CustomEc2Stack --require-approval never"
    7.  Find IP address of new EC2, and plug into browser such as http://<<ip address>
        - The custom index.html page will display if all went well
        - It may take a couple minutes for apache to recognize/load the html page

## Useful commands
 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

