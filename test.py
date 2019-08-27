import boto3 
s3=boto3.client('s3')
b_acl=s3.get_bucket_acl(Bucket='vectortestinfo')
print(b_acl)

