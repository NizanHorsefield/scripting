import boto3
client=boto3.client('elb')
elb_list=client.describe_load_balancers()
for elb in elb_list['LoadBalancerDescriptions']:
    count=len(elb['Instances'])
    print "%s %d" % ( elb['LoadBalancerName'], count)