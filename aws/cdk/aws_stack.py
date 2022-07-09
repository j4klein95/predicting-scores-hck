from aws_cdk import (
    # Duration,
    Stack,
    aws_kms as kms,
    aws_s3 as s3,
    RemovalPolicy,
    aws_lambda as lambda_
    # aws_sqs as sqs,
)
from constructs import Construct


class AwsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        encryption_key = kms.Key(self, 'Key', enable_rotation=True)

        # fix cdk.json to have the region
        bucket = s3.Bucket(self, 'jk-app-cloud-stats-bucket-us-east-1', encryption_key=encryption_key,
                           removal_policy=RemovalPolicy.DESTROY)

        # lambda to run the scraper
        lambda_.DockerImageFunction()
