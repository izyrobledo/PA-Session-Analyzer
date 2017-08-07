import sys, os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import shutil

# arguments that this should take in CL: 
# path (if I need to make new files), region
session = boto3.Session(profile_name = 'default') # this assumes that the user already has a credentials file ... maybe make this more general if necessary 
												  # the session stores configuration state and allows you to create service clients and resources
client = boto3.client('dynamodb', 'us-west-2')
table_name = 'pa0001_session'

dict = {'ssid1': '8e99ce8c75a403b5c163599e23f8b8a6'}
client.get_item(TableName = table_name, Key = {'string': "8e99ce8c75a403b5c163599e23f8b8a6"})




list_of_partitions = session.get_available_partitions() # [u'aws', u'aws-cn', u'aws-us-gov']
print 'List of partitions: '
print list_of_partitions








