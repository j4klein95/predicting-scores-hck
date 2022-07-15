#!/usr/bin/env python3
import aws_cdk as cdk

from cdk.aws_stack import AwsStack

app = cdk.App()

bucket_name = app.node.try_get_context('bucketName')

AwsStack(app, "AwsStack", bucket_name=bucket_name)

app.synth()
