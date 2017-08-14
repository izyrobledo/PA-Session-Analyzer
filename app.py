from flask import Flask, flash, redirect, render_template, request, session, abort
import sys, os
import boto3
from boto3 import s3
from boto3 import dynamodb
from boto3.dynamodb.conditions import Key, Attr
import shutil

from get_AWSInfo import get_AWSInfo

from AWSEnvironment import AWSEnvironment
from dirAndUserInfo import dirAndUserInfo
import time
import datetime


session_list = ['']
app = Flask(__name__)
 
@app.route("/")
def index():
    return "Flask App!"
 
# @app.route("/hello")
# def hello():
#     return "Hello World!"
 
@app.route("/members")
def members():
    return "Members"
 

@app.route("/form/fillOut/", methods=["GET", "POST"])
def hello():


    return render_template(
        'Formv2.html')

@app.route("/form/response/", methods=["GET", "POST"])
def response(): 
    print ' goes to response'
    
    environment = request.form['env']
    ssids = request.form['SSID']
    print 'got env and ssids'
    choice=request.form['userChoice']
    print 'got choice'
    
    print 'this is the user choice: ' + choice
    print type (choice)
    if (choice == 1):
        print 'THE PRINT STATEMENT WORKED'

    #path = '/Users/isabella/Documents/pasessionanalyzer'
    path = os.getcwd()
    aws = get_AWSInfo(choice, environment, path)
   

    # global sesssion_list
    # session_list = aws.mainMethod1(ssids)


    session = boto3.Session(profile_name = 'default')
       
    dynamodb = boto3.resource('dynamodb', aws.region_name)
    s3 = boto3.resource('s3')
    table = dynamodb.Table(aws.session_table)

    
            
    #aws.session_list = ssids.split()
    session_list = aws.choice1(ssids)     

    for ssid in aws.session_list: 
       
        aws.d.makeDirs('/static/', aws.path, ssid)
        # dynamodb = boto3.resource('dynamodb', e.region_name)
        # s3 = boto3.resource('s3')
        # table = dynamodb.Table(e.session_table)
        
        response = table.query(
            KeyConditionExpression=Key('ssid').eq(ssid)
        )
        
       
        img_names = aws.accessInputImages(response, s3)
        hm_img_names = aws.accessHeatMaps(response, s3)
        aws.accessAdditionalInfo(response, ssid)

    #aws.d.zipEverything()

    return render_template(
        'Responsev2.html', choice=choice, environment=environment, session_list = session_list, img_names = img_names, hm_img_names = hm_img_names)
 
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run()