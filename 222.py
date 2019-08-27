import time
import boto3
import paramiko
import socket
import sys
ec2 = boto3.resource('ec2')
ec2.create_instances(ImageId='ami-2d39803a', InstanceType = 't2.micro', MaxCount = 1, MinCount= 1, KeyName='keyPairL1')
for i in ec2.instances.all():
    i.wait_until_running()
    i.load()
for i in ec2.instances.all():
    k =paramiko.RSAKey.from_private_key_file("/home/vcslstudent/Desktop/cc/aws/keyPairL1.pem")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("connecting")
    c.connect(i.public_dns_name, username="ubuntu", pkey=k)
    print("connected")
    commands = ["/home/ubuntu/firstscript.sh", "/home/ubuntu/secondscript.sh"]
    for command in commands:
        print("Executing {}".format(command))
        stdin, stdout, stderr = c.exec_command(command)
        print(stdout.read())
        print("Errors")
        print(stderr.read())
        inp, op, err = c.exec_command('top bn1| grep Cpu')
        print(ec2[i].id + '\t' + op.read())
        time.sleep(5)
c.close()