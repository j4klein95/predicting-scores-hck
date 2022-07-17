import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3 as s3


def get_s3_write_policy(bucket: s3.Bucket) -> iam.PolicyStatement:
    ps = iam.PolicyStatement()
    ps.effect = iam.Effect.ALLOW
    ps.add_actions(
        "s3:PutObject",
        "s3:ListObject",
        "s3:List*"
    )
    ps.add_resources(f'{bucket.bucket_arn}/*')
    ps.add_resources(bucket.bucket_arn)
    return ps
