#Downloads from S3 all the input photos and heatmap images for all SSIDs in a list
#Example usage: python get_session_files_using_list_of_ssids.py /Users/lifanzhang/Downloads/ ct

import sys, os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import shutil
import AWSEnvironment



   
# dev: 3308f8abb23d86014fc226cfa160a8ff

#Example SSID list format:
# session_list = ["58e9da1256333dfffea62ed5ee882149",
# "fbfcb42add8106f48827fef1124b7f4f",
# "d0c7377f3910f3d83f47ecbd3dc96fa0",
# "37fe13f6acc3505e9d057250809550f8",
# "309e635f8c3994a55541b60afc5ff0ef",
# "92cf68d6b1d6fd61741189462748538d",
# "e0fd2fa39f6c419351a0e635fe8d031f",
# "4586cbd98803b1715ac2cdcab28a23f5",
# "aeb19e4ef414de449569b1dd1830b0a7",
# "5230c957cd1f8e8a199cef5da11b049a",
# "455b50cfa095b5d8b586a58398f17ccd",
# "f6d4ca578d2fa9cd5bcb647df3d4fa11",
# "8aad98b6ada8bbe8ca4506b90f5bc085",
# "6689e2b273b3c00d751fef2846193cd5",
# "78e5c0e330258db8a5caeabf95850e85",
# "bec6db8d846d88b0d3295ea6cb33014c",
# "1793512458e8f5c25ff159aaeb151488",
# "94f0099badb023b5fdcb431fd1a932cf",
# "5cb786111aef172070d1d93d72cf91b3",
# "de53c42edcf105aa0b45aa1b029bc826",
# "8e9d21a88ca728e9330f46c8e2103f89",
# "be95b947e6ac4f4e1e34e81d489a7b9e",
# "4cc91dcb7f20fab7fcde6239498e0d1b",
# "aaadd9392bccbb5a6a4385a74742df37",
# "1e3a4e9b8767e7110c9c07f04dec550c",
# "e7224e6367936567f9f5e433614abd5f",
# "d8f0ed725a104f3f11168d7ab3c41296",
# "08a22f0e962280a20b249d4d9f64f4ff",
# "7d605be8c798fc5e5acd97fe6d9ca086",
# "fc15d4ddb49176dbb62a476f74a861ac",
# "a9957cea834447a195113c6bac031d3e",
# "9a892d5e39bb1cc58cfe0b54b33fc8c4",
# "a40c9731e237d0644d415b5ade16539e",
# "0db2505ca0f3299d59ece39da2cd9039",
# "cb6debc5f3ff3ce95e7ddef493393709",
# "467d34e10004b86cf1ab5b605b603b99",
# "a2dea9e7a138b48398805b96fc4b8d87",
# "62d9e89d82f1e6163ec5290d8d9f01ba",
# "dc239ed811d9de61a4a76f2643fafc82",
# "985b8c7b0dba7efc08e76a1ead9afe6e",
# "1b6aff0ddcf9222ec4b5f850454dbe02",
# "65ba13abec355d2fae8e172c61c6c73f",
# "b41cfa5265b5fcbe84bccdd9441dd0ca",
# "7d86fc183d52bd666abe84137df76d0f",
# "68b5964865843977b280e6d16db0ef60",
# "b3daccc98366e97956ed8649683da892",
# "cba0afcf2574b58e36fbeeae844c7906",
# "58af465c1b89332fe1862defbb13166a",
# "093b94f774594b0ced164b3cc0ab1b7c",
# "4e83bfaf03f1577f3b1249a419858a8b",
# "a412c65616dd6873bf2e12c6c3502e27",
# "369b7e74e11ef279e0189bee80640cf4",
# "394043d7921a5fbdca7aea395d189d76",
# "a756fa0a1b61ce7f14ad58c143784cb6",
# "f7a111ca707732a565af75b3f23082f6",
# "00d9a3d8b1abad4074f1b74d2fa5391a",
# "86fc0f2e1ec6991a7f0d9d1a439912bf",
# "bef685228d5bf7f22587a9f5349d9755",
# "dd1c4130242b88f07b93b5addaf2dca8",
# "86c33a79c31cfa0bc4c64febc29cc2d7",
# "ff57e0e672dcd5394fb2e75361aa25fd",
# "2afb1b9f36d372bf3a8e80a203a160f8"]

#add line below.
#aws_access_key_id = ***********LRTA
#aws_secret_access_key = ****************8GZKR

# ***IMPORTANT*** Modify the profile by looking at your ~/.aws/credentials file
# print ("this is isabella's program")

userChoice = input('Would you like to get all the information from one ssid (enter 1), or would you like to query an environment? (enter 2)')
env = raw_input('Enter which environment you would like to work in (dev, qa, or ct): ')
session = boto3.Session(profile_name = 'default')

# if len(sys.argv) != 3:
#     print("Usage: python get_session_files_using_list_of_ssids.py <path> <env>")
#     exit(-1)

path = sys.argv[1]
#env = sys.argv[2]
debug = False
if (debug): print 'debug: ', debug
master_dir = '/s3_files/'



#file_path = sys.argv[3]
#print("File Path: ", file_path)
##Read from an input file containing all SSIDs
#with open(file_path) as f:
#    content = f.readlines()
##Remove whitespace characters like '\n' at the end of each line
#ssids = [x.strip() for x in content]
#print("Adding List of SSIDs: ", ssids)
   
if env == 'ct':
    env = AWSEnvironment()
    parameters = {'session_list':['94ac394ccc50bf2234c59e5e328e4d8d'], 'session_table':'pa1004_session', 's3_image_bucket':'pa_validation-input-ct', 's3_heatmap_bucket':'pa_heatmap_output-ct', 'region_name':'us-east-1'}
    env.envVars(**parameters)
    # session_list = ['94ac394ccc50bf2234c59e5e328e4d8d']
    # session_table = 'pa1004_session'
    # s3_image_bucket = 'pa-validation-input-ct'
    # s3_heatmap_bucket = 'pa-heatmap-output-ct'
    # region_name = 'us-east-1'

elif env == 'qa':
    env = AWSEnvironment(('session_list', ['38cf96644bf96a4203a33ce811a1aec2']), ('session_table', 'pa1001_session'), ('s3_image_bucket', 'pa-validation-input-qa'), ('s3_heatmap_bucket', 'pa-heatmap-output-qa'), ('region_name', 'us-east-1'))

    # session_list = ['38cf96644bf96a4203a33ce811a1aec2']
    # session_table = 'pa1001_session'
    # s3_image_bucket = 'pa-validation-input-qa'
    # s3_heatmap_bucket = 'pa-heatmap-output-qa'
    # region_name = 'us-east-1'

elif env == 'dev':
    env = AWSEnvironment(('session_list', ['e64a01676f602cc660cb9324b668e0f3', '8e99ce8c75a403b5c163599e23f8b8a6', '4d5553375cf049a3295a769b3681facf']), ('session_table', 'pa0001_session'), ('s3_image_bucket', 'pa-validation-input'), ('s3_heatmap_bucket', 'pa-heatmap-output'), ('region_name', 'us-west-1'))


    # session_list = ['e64a01676f602cc660cb9324b668e0f3', '8e99ce8c75a403b5c163599e23f8b8a6', '4d5553375cf049a3295a769b3681facf']
    # session_table = 'pa0001_session'
    # s3_image_bucket = 'pa-validation-input'
    # s3_heatmap_bucket = 'pa-heatmap-output'
    # region_name = 'us-west-2'


#for ssid in ssids:
for ssid in session_list: 
    
    directory = path + master_dir + ssid #path to 'new' file s3_files(master_dir) and another file within that is the ssid file
    input_dir = directory + '/Input/' #path to '/Input' file within the ssid file
    nitro_heatmaps_dir = directory + '/Nitro_Heatmaps/' #path to '/Nitro_Heatmaps' file within the ssid file
    zip_input_dir = path + master_dir #path to input zip inside of s3_files

    zip_output_dir = path + '/s3_zip/' #path to zip located where the code is 
    
    if not os.path.exists(directory):
      os.makedirs(directory)
    if not os.path.exists(input_dir):
      os.makedirs(input_dir)
    if not os.path.exists(nitro_heatmaps_dir):
      os.makedirs(nitro_heatmaps_dir)
      
    dynamodb = boto3.resource('dynamodb', env.region_name)
    s3 = boto3.resource('s3')

    
    table = dynamodb.Table(env.session_table)
    
    response = table.query(
      KeyConditionExpression=Key('ssid').eq(ssid)
    )


   
     

    #try to print response .... different array configs
    
    #print response
    
    #img_keys = map(lambda x: (x['image_name'],x['validation_status']), response['Items'][0]['input_images'])
    # ^^ goes through all the input images in the input_image list 
    #print "Img Keys: ", img_keys
    
    # print "\n"

    # print "\n\nresponse['Items']"
    # print response['Items']

    # print '\n\n'

    # print "response['Items'][0]"
    # print response['Items'][0]

    # print "\n"

    # print "response['Items'][0]['input_images']"
    # print response['Items'][0]['input_images']

    # print "\n"


    # print "response['Items'][0]['input_images'][0]"
    # print response['Items'][0]['input_images'][0]

    print "\nSSID: ", ssid

    # get input images for a specific ssid
    try: 
       
       for individual_images in response['Items'][0]['input_images']: 
         
         if (debug): 
            print "individual_images --> ", individual_images # prints the entire row for that particular image
         img_name = individual_images['image_name'] #  gets the name of the image from that row
         if (debug): 
            print "\timage name --> ", img_name # prints name
         image = s3.Object(env.s3_image_bucket, str(img_name + '.jpg')) # makes an s3 object (if I understand correctly) 
         if (debug): 
            print '\timage --> ', image
         image.download_file(input_dir + (img_name) + '.jpg') # downloads the file from s3 
         if debug: print '\tinput_dir --> ', input_dir
       print 'This ssid has the appropriate input images, they have been downloaded to', input_dir
    except: 
      print 'This ssid does not have the relevant input images'
   



    # get heat maps for individual images
    try: 
       
       for individual_heatmaps in response['Items'][0]['heat_maps']:
         
         if (debug): print "individual heatmaps --> ", individual_heatmaps
         heatmap_name = str(individual_heatmaps['file_name'])
         if (debug): print "\theatmap name --> ", heatmap_name
         heatmap_image = s3.Object(env.s3_heatmap_bucket, heatmap_name) # ('bucket_name', 'key')
         if (debug): print "\theatmap_image --> ", str(heatmap_image)
         heatmap_image.download_file(nitro_heatmaps_dir + heatmap_name )
         if (debug): print '\tnitro_heatmaps_dir --> ', nitro_heatmaps_dir
       print 'This ssid has the appropriate heatmaps, they have been downloaded to', nitro_heatmaps_dir
    except:
      print 'This ssid does not have the relevant heat maps'

    # about the crash: airbagDeployed, drivable, [estimate (Map): amount, create_ts], heat_maps (map of 4 images), input_images (map of 4 images),                    
    # about the kind of car: bodyTypeCode, displayModel, modelYear, odometerReading, stateInspectionCode, VIN
    # about the user: ownerZip, platformName, platformVersion, sessionCreateTs, ssid, userID
    # about the sesh: uploadClaims,
    # not sure about: carrierId, clientVersion, featureVector (Map of 31 items), makeDesc
    #                 motorChapterId, primaryImpactCode, releaseVersion, secondaryDamage, secondaryImpactCode, surveyResponse (List of 2, each index of list has a map of 2 with the answerId and questionId)
    #                 trimLevel, 

    # about the crash: 
    try: 
      print 'Was the airbag deployed?  ', response['Items'][0]['airbagDeployed']
    except:
      print 'this ssid does not have the airbagDeployed field'

    try: 
      print 'Is the car drivable?  ', response['Items'][0]['drivable']
    except: 
      print 'this ssid does not have the drivable field'

    try: 
      print 'What is the estimate for the damage?  ', response['Items'][0]['estimate']['amount']
    except: 
      print 'this ssid does not have the estimate field'

    try: 
      print 'When was the estimate created?  ', response['Items'][0]['estimate']['create_ts']
    except: 
      print 'this ssid does not have the time stamp for the estimate'

    # about the kind of car: 
    

    

shutil.make_archive(zip_output_dir, 'zip', zip_input_dir)

#s3.Object('pa-validation-input-qa', '0002641c-24bf-48b0-9551-d51dec2e65ab.jpg').download_file('/tmp/foo1.jpg')