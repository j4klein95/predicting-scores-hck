#!/usr/bin/env python3
import aws_cdk as cdk

from cdk.prdct_hcky import PrdctHckyApp

app = cdk.App()

bucket_name = app.node.try_get_context('bucketName')

PrdctHckyApp(app, "PrdctHckyApp", bucket_name=bucket_name)

app.synth()
