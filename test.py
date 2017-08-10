from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_s3 import FlaskS3
import sys, os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import shutil
from AWSEnvironment import AWSEnvironment
import time
import dirAndUserInfo
from dirAndUserInfo import dirAndUserInfo
from get_AWSInfo import get_AWSInfo


choice=1    
environment="dev"
ssid = "f37fadbab174526fef3adc45b86ae7b5"

path = '/Users/isabella/Documents/workspace/pasessionanalyzer'
    # '/Users/isabella/Documents/workspace/pasessionanalyzer'
aws = get_AWSInfo(choice, environment, ssid, path) # <-- get all these variables

aws.defineEnvironments() # <-- define environment variables


dynamodb = boto3.resource('dynamodb', aws.region_name)
s3 = boto3.resource('s3')
#s3 = boto3.client ('s3')
table = dynamodb.Table(aws.session_table)

for ssid in aws.list_ssids:
            # if not os.path.exists(self.directory):
            #     os.makedirs(self.directory)
    print ssid
    print "\n"
    aws.d.makeDirs('/s3_files/', path, ssid)
            # dynamodb = boto3.resource('dynamodb', e.region_name)
            # s3 = boto3.resource('s3')
            # table = dynamodb.Table(e.session_table)
    response = table.query(
        KeyConditionExpression=Key('ssid').eq(ssid)
    )
    
    input_images = aws.accessInputImages(response, s3)
    heatmaps = aws.accessHeatMaps(response, s3)
    aws.accessAdditionalInfo(response, ssid)