import sys,time
import boto3, paramiko
# Monitor CPU usage of two instances
ec2 = boto3.resource('ec2')
instances = ec2.instances.filter(Filters=[{'Name':'instance-state-name','Values' : ['running']}])
def monitor(instances):

 shellsList = []
 dockerImageList = []
 for idx,instance in enumerate(instances):

  try:
   secureShell = paramiko.SSHClient()
   secureShell.set_missing_host_key_policy(paramiko.AutoAddPolicy())

   secureShell.connect(instance.public_dns_name,username="ec2-user",pkey=paramiko.RSAKey.from_private_key_file("/home/shamanthaka/vinnykey2018.pem"))
   if secureShell is not None:
     shellsList.append(secureShell)
   secureShell.exec_command('sudo docker run -d -t ec2-user sh')
   stdin, output, error = secureShell.exec_command('sudo docker ps | grep ec2-user')
   dockerImageList.append(output.read().strip().split('\n'))
  except Exception as e:
   print('error encountered. Exiting.' + e)
   exit(1)
# create new list with name repeated twice, to map to each docker container
 ec2Dockers =[instances[0], instances[0], instances[1], instances[1]]
 secureShellDockers = [shellsList[0], shellsList[0], shellsList[1], shellsList[1]]
 try:
  while True:
   for (ec2, secureShell, dockerimage) in zip(ec2Dockers, secureShellDockers,dockerImageList):
    stdin, output, error = secureShell.exec_command('sudo docker exec ' +str(dockerimage) + ' top-bn2 | grep Cpu:')
    print(ec2.id + '\t' + dockerimage + '\t' + output.read())
    print('---')
  time.sleep(5)
 except Exception as e:
  print('Exiting. ' + e.message)
  exit(1)


if __name__ == '__main__':
 print('\nMonitor Tool\n---')
 monitor(list(instances))
