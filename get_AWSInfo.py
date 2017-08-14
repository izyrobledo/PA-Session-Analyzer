### old one
import sys, os
import boto3
from boto3 import s3
from boto3 import dynamodb
from boto3.dynamodb.conditions import Key, Attr
import shutil
from AWSEnvironment import AWSEnvironment
from dirAndUserInfo import dirAndUserInfo
import time
import datetime

 

class get_AWSInfo:

    choice = ''
    env = ''
    list_ssid = []


    session_list = []
    session_table = ''
    s3_image_bucket = ''
    s3_heatmap_bucket = ''
    region_name = ''


    session_list = []
    session_table = ''
    s3_image_bucket = ''
    s3_heatmap_bucket = ''
    region_name = ''

    d = ''

    



    def __init__(self, choice, env, path):
        self.choice = choice
        
        self.env = env
        self.path = path
        self.defineEnvironments()
        self.d = dirAndUserInfo()


    def accessInputImages(self,response, s3):
        debug = False
        img_names = []
        # get input images for a specific ssid
        try: 
           for individual_images in response['Items'][0]['input_images']: 
             if (debug): print "individual_images --> ", individual_images # prints the entire row for that particular image
             img_name = individual_images['image_name'] #  gets the name of the image from that row
             if (img_name[-4:] != '.jpg'):
                img_name = img_name + '.jpg'
             img_names.append(img_name)
             if (debug): print "\timage name --> ", img_name # prints name
             image = s3.Object(self.s3_image_bucket, str(img_name )) # makes an s3 object (if I understand correctly) 
             
             image.download_file(self.d.directory + img_name)
             
             if (debug): print 'This ssid has the appropriate input images, they have been downloaded to', self.d.directory
        except: 
          if (debug): print 'This ssid does not have the relevant input images'

        return img_names

    def accessHeatMaps(self, response, s3):
        debug = False
        hm_img_names = []
        try:
            for individual_heatmaps in response['Items'][0]['heat_maps']:
                if (debug): print "individual heatmaps --> ", individual_heatmaps
                heatmap_name = str(individual_heatmaps['file_name'])
                if (debug): print "\theatmap name --> ", heatmap_name
                hm_img_names.append(heatmap_name)
                heatmap_image = s3.Object(self.s3_heatmap_bucket, heatmap_name) # ('bucket_name', 'key')
                if (debug): print "\theatmap_image --> ", str(heatmap_image)
                #heatmap_image.download_file(self.d.nitro_heatmaps_dir + heatmap_name )
                heatmap_image.download_file(self.d.directory + heatmap_name )
                

            if (debug): print 'This ssid has the appropriate heatmaps, they have been downloaded to', self.d.directory
        except:
            if (debug): print 'This ssid does not have the relevant heatmap images'
        return hm_img_names

    def accessAdditionalInfo(self, response, ssid):

        # about the crash: airbagDeployed, drivable, [estimate (Map): amount, create_ts], heat_maps (map of 4 images), input_images (map of 4 images),                    
        # about the kind of car: bodyTypeCode, displayModel, modelYear, odometerReading, stateInspectionCode, VIN
        # about the user: ownerZip, platformName, platformVersion, sessionCreateTs, ssid, userID
        # about the sesh: uploadClaims,
        # not sure about: carrierId, clientVersion, featureVector (Map of 31 items), makeDesc
        #                 motorChapterId, primaryImpactCode, releaseVersion, secondaryDamage, secondaryImpactCode, surveyResponse (List of 2, each index of list has a map of 2 with the answerId and questionId)
        #                 trimLevel, 
        nameOfFile = ssid+'_FNOL.txt'
        completeName = os.path.join(self.d.directory, nameOfFile)
        f= open(completeName,"w+")
        attributes = ['modelYear', 'makeDesc', 'displayModel', 'trimLevel', 'odometerReading', 'ownerZip', 'primaryImpactCode', 'airbagDeployed', 'drivable', 'uploadClaims', 'sessionCreateTs', 'carrierId']
        for attr in attributes: 
            f.write (attr)
            f.write (', ')
        f.write ('estimate')
        f.write('\n')

        for attr in attributes:
            try:
                f.write(response['Items'][0][attr])
                f.write(', ')
            except:
                f.write('NA, ')

        try: 
            f.write(response['Items'][0]['estimate']['amount'])
        except:
            f.write('NA')


    def defineEnvironments(self):
        if self.env == 'ct':
            #e = AWSEnvironment('pa1004_session', 'pa_validation-input-ct', 'pa_heatmap_output-ct', 'us-west-2')
            self.session_table = 'pa1004_session'
            self.s3_image_bucket = 'pa-validation-input-ct'
            self.s3_heatmap_bucket = 'pa_heatmap_output-ct'
            self.region_name = 'us-east-1'
            # 45c95fad36838e24a046e7dde0f56655 94ac394ccc50bf2234c59e5e328e4d8d ca9a66875968feb1d595cf14eca3268a
        elif self.env == 'qa':
            #e = AWSEnvironment('pa1001_session', 'pa-validation-input-qa', 'pa-heatmap-output-qa', 'us-east-1')
            self.session_table = 'pa1001_session'
            self.s3_image_bucket = 'pa-validation-input-qa'
            self.s3_heatmap_bucket = 'pa-heatmap-output-qa'
            self.region_name = 'us-east-1'
            # ['38cf96644bf96a4203a33ce811a1aec2']
        elif self.env == 'dev':
            #e = AWSEnvironment('pa0001_session', 'pa-validation-input', 'pa-heatmap-output', 'us-west-2')
            self.session_table = 'pa0001_session'
            self.s3_image_bucket = 'pa-validation-input'
            self.s3_heatmap_bucket = 'pa-heatmap-output'
            self.region_name = 'us-west-2'
            # e288209058f052fb268e31432e1ceb8b 4d5553375cf049a3295a769b3681facf df29e781b15bb6fa45c875cebf487387
        

    def getSSIDsInRange(self): 

        debug = False
        lessThanOrGreater = input('Would you like a list of ssids greater than a given time stamp (enter 1), less than a given time stamp (enter 2), or between two time stamps (enter 3)')
        
        if (lessThanOrGreater == 1 ):
            timeStamp = raw_input('Please enter the time stamp cut off you would like to use, you will get all the ssids in this environment with a sessionCreateTs greater than the one entered: ')
            response = table.scan( # response is a list of all the thigns that satisfy the filter below
                FilterExpression=Attr('sessionCreateTs').gt(timeStamp)
                # 2017-06-19 06:27:50
            )
        elif (lessThanOrGreater == 2):
            timeStamp = raw_input('Please enter the time stamp cut off you would like to use, you will get all the ssids in this environment with a sessionCreateTs less than the one entered: ')
            response = table.scan( # response is a list of all the thigns that satisfy the filter below
                FilterExpression=Attr('sessionCreateTs').lt(timeStamp)
                # 2017-08-19 06:14:38
            )
        elif (lessThanOrGreater == 3):
            timeStamps = raw_input('Please enter the two time stamps you would like to use, you will get all the ssids that have a sessionCreateTs between these times (seperated by a space_: ')
            timeStampList = timeStamps.split()
            response = table.scan(
                FilterExpression = Attr('sessionCreateTs').between(timeStampList[0]+timeStampList[1], timeStampList[2]+timeStampList[3])
            )
            # 2017-06-19 06:27:50 2017-08-19 06:14:38

    
        for ssid in response['Items']:  # we have to specify that we are looking through the ['Items'] key in response because response
                                         # also has a ['Count'], ['LastEvaluatedKey'], ['ScannedCount'] key ... etc response['Items'] is a 
                                         # a list of all the ssids that match the filter 
            if (debug): print "ssid: "+ssid['ssid'] +", sessionCreateTs: "+ssid['sessionCreateTs']
            #print '\n'

    def choice1(self, ssids):

        self.session_list = ssids.split()

        return self.session_list
 