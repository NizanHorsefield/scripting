import boto3
from datetime import datetime, timedelta
region = "eu-west-1"
ec2 = boto3.resource("ec2", region_name=region)
def get_available_volumes():
    available_volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
    return available_volumes
    print available_volumes


def get_snapshots_filter(self):

    return [{
        'Name': 'status',
        'Values': [
            'completed',
        ]}, {
        'Name': 'description',
        'Values': [
            'Created by CreateImage*'
        ]
    }]

get_snapshots_filter(self)