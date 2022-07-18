import aws_cdk
from aws_cdk import (
    Stack,
    aws_kms as kms,
    aws_s3 as s3,
    RemovalPolicy,
    aws_lambda as lambda_,
)
from constructs import Construct


class AwsStack(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 bucket_name: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        encryption_key = kms.Key(self, 'Key', enable_key_rotation=True)

        # fix cdk.json to have the region
        bucket = s3.Bucket(self, 'jk-app-cloud-stats2-bucket-us-east-1', encryption_key=encryption_key,
                           removal_policy=RemovalPolicy.DESTROY, bucket_name=bucket_name)

        # lambda to run the scraper
        lambda_.DockerImageFunction(self,
                                    'jk-app-cloud-stats-scraper-lambda',
                                    code=lambda_.DockerImageCode.from_image_asset('../engineering/lambda'),
                                    function_name='predicting-scores-hcky-scraping-lambda',
                                    environment={"bucket": bucket.bucket_name},
                                    timeout=aws_cdk.Duration.seconds(300),
                                    memory_size=5000,
                                    ephemeral_storage_size=aws_cdk.Size.mebibytes(512)
                                    )
