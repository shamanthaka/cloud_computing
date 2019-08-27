import boto3

def start_instances(num_instances):
    ec2 = boto3.resource('ec2')
    ec2.create_instances(ImageId='ami-013be31976ca2c322', InstanceType = 't2.micro', MaxCount =
    num_instances, MinCount = 1, KeyName='vinnykey2018')
    for i in ec2.instances.all():
        i.wait_until_running()
    for i in ec2.instances.all():
        print(i.id, i.state)
start_instances(5)
