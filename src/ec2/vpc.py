class VPC:
    def __init__(self, client):
        self._client = client
        """:type : pyboto3.ec2 """

    def create_vpc(self):
        print("Creating a VPC...")
        return self._client.create_vpc(
            CidrBlock='10.0.0.0/16'
        )

    def add_name_tag(self, resource_id, resource_name):
        print('Adding ' + resource_name + ' tag to the ' + resource_id)
        return self._client.create_tags(
            Resources=[resource_id],
            Tags=[{
                'Key': 'Name',
                'Value': resource_name
            }]
        )

    def create_internet_gateway(self):
        print('Creating an Internet Gateway ')
        return self._client.create_internet_gateway()

    def attach_ig_to_vpc(self, vpc_id, ig_id):
        print("Attaching Internet Gateway " + ig_id + " to vpc " + vpc_id)
        return self._client.attach_internet_gateway(
            InternetGatewayId=ig_id,
            VpcId=vpc_id
        )

    def create_subnet(self,vpc_id, cidr_block):
        print("Creating a subnet for VPC " + vpc_id + " to VPC " + vpc_id)
        return self._client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block
        )

    def create_public_route_table(self, vpc_id):
        print("Creating public route table for VPC " + vpc_id)
        return self._client.create_route_table(VpcId=vpc_id)

    def create_ig_route_to_public_route_table(self, rt_id, ig_id):
        print("Created route table " + rt_id + " with internet gateway " + ig_id)
        return self._client.create_route(
            RouteTableId=rt_id,
            GatewayId=ig_id,
            DestinationCidrBlock='0.0.0.0/0'
        )

    def associate_subnet_with_route_table(self, subnet_id, rt_id):
        print("Associated subnet " + subnet_id + " with route table " + rt_id)
        return self._client.associate_route_table(
            SubnetId=subnet_id,
            RouteTableId=rt_id
        )

    def allow_auto_assign_ip_addresses_for_subnet(self, subnet_id):
        print("Auto assign ip addresses for subnet " + subnet_id)
        return self._client.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={'Value': True}
        )