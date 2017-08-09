from flask import Flask, flash, redirect, render_template, request, session, abort
from get_AWSInfo import get_AWSInfo

import sys, os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import shutil
from AWSEnvironment import AWSEnvironment
from dirAndUserInfo import dirAndUserInfo
import time
import datetime
# import get_AWSInfo
# import dirAndUserInfo
# import AWSEnvironment
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


@app.route("/form/fillOut/", methods = ["GET", "POST"])
def hello():
    return render_template('Formv2.html')


@app.route("/form/response/", methods = ["GET", "POST"])
def response():

    choice=request.form['userChoice']
    environment=request.form['env']
    ssid=request.form['SSID']

    path = '/Users/isabella/Documents/workspace/pasessionanalyzer'
    aws = get_AWSInfo(choice, environment, ssid, path)

    aws.defineEnvironments()
    print 'region name !!!!!: '+ aws.region_name

    dynamodb = boto3.resource('dynamodb', aws.region_name)
    s3 = boto3.resource('s3')
    table = dynamodb.Table(aws.session_table)

    if (choice == '1'):
        print 'choice is 1'
        aws.goThroughSSIDS(dynamodb, s3, table)
    elif (choice == 2):
        aws.getSSIDsInRange()

    return render_template('Responsev2.html', choice=choice, environment=environment, ssid=ssid)



if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run()




