import boto3
import sys
import time

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

#AWS Account and Region Definition for Reboot Actions
akid = '445189663936'
region = 'eu-west-1'

#Create Session with IAM User
session = boto3.session.Session()

#Create AWS clients
cw = session.client('cloudwatch')
ec2 = boto3.resource('ec2')


def find():

    alarms = cw.describe_alarms(StateValue='INSUFFICIENT_DATA',MaxRecords=100)

    insuff_alarms = []
    loops = 1

    insuff_alarms.extend(alarms['MetricAlarms'])
    while ('NextToken' in alarms):
        alarms = cw.describe_alarms(StateValue='INSUFFICIENT_DATA',MaxRecords=100,NextToken=alarms['NextToken'])
        #print('on loop',loops,'alarms is',alarms)
        insuff_alarms.extend(alarms['MetricAlarms'])
        loops += 1

    print('Looped',loops,'times to generate list of ',len(insuff_alarms),'alarms in state INSUFFICIENT_DATA.')

    instances = [instance for instance in ec2.instances.all()]
    instance_ids = [instance.id for instance in instances]
    print('We have',len(instance_ids),'instances in our account right now.')
    #print(instance_ids)

    state_dict = {}

    for inst in ec2.instances.all():
        state = inst.state['Name']
        if state in state_dict:
            state_dict[state] += 1
        else:
            state_dict[state] = 1
    print(state_dict)

    ###################################################
    #Find and delete orphan alarms
    ###################################################
    our_dim = 'InstanceId'
    num_orphan_alarms = 0

    for insuff_alarm in insuff_alarms:
        #Dimensions is a list of dicts.
        dims = insuff_alarm['Dimensions']
        #print(dim)
        #print(insuff_alarm)
        #print(insuff_alarm,insuff_alarm.namespace,insuff_alarm.dimensions)
        inst_id = ''
        for dim in dims:
            #dim is a dict with two key/values:  Name and Value.  (yes, it's confusing.  Welcome to boto3)
            if dim['Name'] == our_dim:
                inst_id = dim['Value']

        if inst_id:
            #this is an instance-level alarm
            #print(insuff_alarm.dimensions)
            if (inst_id not in instance_ids):
                #This is an alarm for an instance that doesn't exist
                name = insuff_alarm['AlarmName']
                prRed('Alarm' + name + "is for an instance that doesn't exist:" + inst_id)
                #cw.delete_alarms(AlarmNames=[name])
                num_orphan_alarms += 1
        else:
            #print(insuff_alarm.keys())
            print(insuff_alarm['AlarmName'],'has dimensions',dims)

    print(num_orphan_alarms,'orphan alarms found and deleted.')

find()
