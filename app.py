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
    
    choice=request.form['userChoice']
    environment = request.form['env']
    path = os.getcwd()
    aws = get_AWSInfo(choice, environment, path)

    dynamodb = boto3.resource('dynamodb', aws.region_name)
    s3 = boto3.resource('s3')
    table = dynamodb.Table(aws.session_table)
    if (choice == u'1'):

        
        ssids = request.form['SSID']
        session = boto3.Session(profile_name = 'default')
        session_list = aws.choice1(ssids)     

        for ssid in aws.session_list: 
           
            aws.d.makeDirs('/static/', aws.path, ssid)
            response = table.query(
                KeyConditionExpression=Key('ssid').eq(ssid)
            )
            
           
            img_names = aws.accessInputImages(response, s3)
            hm_img_names = aws.accessHeatMaps(response, s3)
            FNOL_dict = aws.accessAdditionalInfo(response, ssid)
        return render_template(
            'Responsev2.html', FNOL_dict = FNOL_dict, choice=choice, environment=environment, session_list = session_list, img_names = img_names, hm_img_names = hm_img_names)
    
    elif (choice == u'2'):
        environment = request.form['env']
        lessThanOrGreater = request.form['lessThanOrGreater']
        timeStamps = request.form['timeStamps']

        listOfSSIDs = aws.getSSIDsInRange(lessThanOrGreater, timeStamps, table)

        return render_template(
            'Response2.html', choice=choice, environment=environment, listOfSSIDs = listOfSSIDs)
    
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run()