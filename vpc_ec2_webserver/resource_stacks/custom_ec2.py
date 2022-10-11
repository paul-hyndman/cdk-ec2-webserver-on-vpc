from aws_cdk import (
    core,
    aws_ec2 as _ec2,
    aws_iam as _iam
)
from constructs import Construct


class CustomEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read bootstrap script to install Apache and copy index.html from S3
        with open("user-data/install_httpd.sh", mode="r") as file:
            user_data = file.read()

        # Get latest ami
        amzn_linux_ami = _ec2.MachineImage.latest_amazon_linux(
            generation=_ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
            edition=_ec2.AmazonLinuxEdition.STANDARD,
            storage=_ec2.AmazonLinuxStorage.EBS,
            virtualization=_ec2.AmazonLinuxVirt.HVM
        )

        # Use VPC created earlier
        vpc = _ec2.Vpc.from_lookup(self,
                                   "importedVPC",
                                   # Use console to find ID previously created VPC
                                   vpc_id="vpc-0d6b43939b42ef7b4")

        # Create EC2 instance
        web_server = _ec2.Instance(self,
                                   "webserverId",
                                   instance_type=_ec2.InstanceType(instance_type_identifier="t2.micro"),
                                   instance_name="WebServer001",
                                   machine_image=amzn_linux_ami,
                                   vpc=vpc,
                                   vpc_subnets=_ec2.SubnetSelection(
                                       subnet_type=_ec2.SubnetType.PUBLIC
                                   ),
                                   user_data=_ec2.UserData.custom(user_data),
                                   )

        # Add additional EBS Storage which is not required here, but useful when user data
        # loads JDKs or other large files
        web_server.instance.add_property_override(
            "BlockDeviceMappings", [
                {
                    "DeviceName": "/dev/sdb",
                    "Ebs": {
                        "VolumeSize": "50",
                        "DeleteOnTermination": "true"
                    }
                }
            ]
        )

        core.CfnOutput(self,
                       "webServer001Ip",
                       description="WebServer Public Ip Address",
                       value=f"http://{web_server.instance_public_ip}")

        # Allow incoming web traffic
        web_server.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(80), description="Allow incoming web traffic"
        )

        # Add permission to web server instance profile.  Not required here, but useful
        web_server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )

        # Useful if your application reads from S3 buckets, but not required here
        web_server.role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                # In prod this would be custom policy vs. policy allowing read from any S3
                "AmazonS3ReadOnlyAccess"
            )
        )
