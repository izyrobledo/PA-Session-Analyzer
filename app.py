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
        'form.html')

@app.route("/form/response/", methods=["GET", "POST"])
def response(): 

    choice=request.form['userChoice']
    environment = request.form['env']
    ssids = request.form['SSID']
    


    #path = '/Users/isabella/Documents/pasessionanalyzer'
    path = os.getcwd()
    aws = get_AWSInfo(choice, environment, path)
    print '4'

    global sesssion_list
    session_list = aws.mainMethod1(ssids)
    print '5'

    return render_template(
        'response.html', choice=choice, environment=environment, session_list = session_list)
 
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=80)
    app.run()