import boto3
import botocore

def copy_objects():

    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket='shamanthaka30')
    mybucket = s3.Bucket('shamanthaka30')
    mybucket.Acl().put(ACL='public-read-write')
    exists = True

    try:
        s3.meta.client.head_bucket(Bucket='wsu2017fall')
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            exists = False
            print("contents of Bucket: wsu2017fall")

    wsubucket = s3.Bucket('wsu2017fall')
    exists = True


    for key in wsubucket.objects.all():
        print(key.key)
    for k in wsubucket.objects.all():
        try:
            print (k.get()['Body'].read())
            copyfrom={'Bucket':'wsu2017fall','Key':'data/FireAndIce'}
            s3.meta.client.copy(copyfrom,'shamanthaka30','shamanthaka30/fireandice')
        except:
            pass


copy_objects()