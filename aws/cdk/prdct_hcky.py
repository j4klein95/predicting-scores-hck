import aws_cdk
from aws_cdk import (
    Stack,
    aws_kms as kms,
    aws_s3 as s3,
    RemovalPolicy,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks
)
from constructs import Construct

from .iam_helpers import get_s3_write_policy


class PrdctHckyApp(Stack):

    def __init__(self,
                 scope: Construct,
                 construct_id: str,
                 bucket_name: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        encryption_key = kms.Key(self, 'Key', enable_key_rotation=True)

        # fix cdk.json to have the region
        bucket = s3.Bucket(self, 'jk-app-cloud-stats-bucket-us-east-1', encryption_key=encryption_key,
                           removal_policy=RemovalPolicy.DESTROY, bucket_name=bucket_name)

        # lambda to run the scraper for basic stats
        basic_stats_lambda = lambda_.DockerImageFunction(self,
                                                         'basic-stats-scraper-lambda',
                                                         code=lambda_.DockerImageCode.from_image_asset(
                                                             '../engineering/basic-stats-lambda'),
                                                         function_name='hcky-basic-stats-scraper-lambda',
                                                         environment={"bucket": bucket.bucket_name},
                                                         timeout=aws_cdk.Duration.seconds(300),
                                                         memory_size=5000,
                                                         ephemeral_storage_size=aws_cdk.Size.mebibytes(512),
                                                         )

        encryption_key.grant_encrypt_decrypt(basic_stats_lambda.role)
        basic_stats_lambda.add_to_role_policy(get_s3_write_policy(bucket=bucket))

        # lambda to run the scraper for advanced stats
        advanced_stats_lambda = lambda_.DockerImageFunction(self,
                                                            'advanced-stats-scraper-lambda',
                                                            code=lambda_.DockerImageCode.from_image_asset(
                                                                '../engineering/advanced-stats-lambda'),
                                                            function_name='hcky-advanced-stats-scraper-lambda',
                                                            environment={"bucket": bucket.bucket_name},
                                                            timeout=aws_cdk.Duration.seconds(300),
                                                            memory_size=5000,
                                                            ephemeral_storage_size=aws_cdk.Size.mebibytes(512),
                                                            )

        encryption_key.grant_encrypt_decrypt(advanced_stats_lambda.role)
        advanced_stats_lambda.add_to_role_policy(get_s3_write_policy(bucket=bucket))

        # StepFunction - State Machine Definition
        basic_stats_job = tasks.LambdaInvoke(
            self,
            "Scrape Basic Hockey Stats",
            lambda_function=basic_stats_lambda,
            output_path="$.Payload",
            retry_on_service_exceptions=True
        )

        advanced_stats_job = tasks.LambdaInvoke(
            self,
            "Scrape Advanced Hockey Stats",
            lambda_function=advanced_stats_lambda,
            output_path="$.Payload",
            retry_on_service_exceptions=True
        )

        parallel = sfn.Parallel(self, "Scrape Stats in parallel", result_path='$.status')
        parallel.branch(basic_stats_job)
        parallel.branch(advanced_stats_job)
        parallel.add_retry(interval=aws_cdk.Duration.seconds(30), max_attempts=2)

        fail_job = sfn.Fail(
            self, "Fail", error="$.error", cause="An exception was raised."
        )

        succeed_job = sfn.Succeed(
            self, "Succeeded", comment='Dataload completed'
        )

        definition = sfn.Chain.start(parallel)

        sfn.StateMachine(self,
                         "hcky-mini-lake-loader-sfn",
                         definition=definition,
                         timeout=aws_cdk.Duration.minutes(10)
                         )
