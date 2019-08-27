import sys
import time
import boto3
import paramiko
import socket


def run_instances(num_instances):

	try:
         ec2 = boto3.resource('ec2')
         instances_created = ec2.create_instances(ImageId="ami-013be31976ca2c322",InstanceType ="t2.micro",MinCount = num_instances,\
                                                  MaxCount = num_instances,KeyName="vinnykey2018",SecurityGroupIds=["sg-007443309ef409a2a"])
         print("Waiting for the instances to start")
         for instance in instances_created:
             instance.wait_until_running()
             instance.reload()
         for instance in instances_created:
             print(instance.id, instance.state)
         print("Instances Created!!")
         time.sleep(80)
         return instances_created
	except:
	    print("Could not create the Instances. Please run the program again! ")

def monitor(ec2):

    shellsList = []
    for e in ec2:
        try:

        #Creating client shell for instances
            clientShells = paramiko.SSHClient()
            clientShells.load_system_host_keys()
            clientShells.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            k = paramiko.RSAKey.from_private_key_file("/home/shamanthaka/vinnykey2018.pem")
            clientShells.connect(e.public_dns_name,username="ec2-user",key_filename="/home/shamanthaka/vinnykey2018.pem")
            if clientShells is not None:
                shellsList.append(clientShells)
        except Exception as e:
            print("Error encountered. Exiting." + e.message)
            exit(1)
        try:
            while True:

                for i, clientShells in enumerate(shellsList):

                    inp, op, err = clientShells.exec_command("top bn2 | grep Cpu")
                    print(ec2[i].id + '\t' + str(op.read()))
                    time.sleep(5) #Wait for 5 seconds untill next command execution
        except Exception as e:
            print("Exiting. " + e.message)
            exit(1)


if __name__ == '__main__':

     print("\n Monitor Tool")
     monitor(list(run_instances(2)))
