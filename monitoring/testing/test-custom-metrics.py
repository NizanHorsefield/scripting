from boto.ec2.cloudwatch import connect_to_region
import sys
import boto.ec2.cloudwatch

reg='eu-west-1'
metric=sys.argv[1]
server = sys.argv[2]

conn_cw=boto.ec2.cloudwatch.connect_to_region(reg)
conn_cw.put_metric_data(namespace='JvmMetrics',name='JvmHoggingThreadCount',value=metric,dimensions={'ManagedServer':server})
