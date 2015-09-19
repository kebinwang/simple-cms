import boto3

from StringIO import StringIO


class S3:
    BUCKET = "simple-cms"

    def __init__(self):
        self._client = boto3.client('s3')

    def get(self, key):
        try:
            return str(self._client.get_object(Bucket=S3.BUCKET, Key=key)["Body"].read())
        except:
            return None

    def set(self, key, value):
        self._client.put_object(Body=StringIO(value), Key=key, Bucket=S3.BUCKET, ACL='public-read')


s3 = S3()
