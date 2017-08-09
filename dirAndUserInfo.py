import sys, os
import shutil

class dirAndUserInfo:


    import sys, os
    
   
    
    ssid = ''
    directory = ''
    input_dir = ''
    nitro_heatmaps_dir = ''
    zip_input_dir = ''
    zip_output_dir = ''

    userChoice = ''
    env = ''
    list_ssids = ['']

    def __init__(self):
        self.master_dir = '/s3_files/'
        
    def getUserInput(self):
        self.userChoice = input('Would you like to get all the information from one ssid (enter 1), or would you like to query an environment? (enter 2)')
        print type (self.userChoice)
        if (self.userChoice == 1):
            self.env = raw_input('Enter which environment you would like to work in (dev, qa, or ct): ')
            string_input = raw_input('Which ssids would you like information on? Enter each ssid seperated by a space: ')
            self.list_ssids = string_input.split()
        if (self.userChoice == 2):
            self.env = raw_input('Enter which environment you would like to work in (dev, qa, or ct): ')


    def makeDirs(self, master_dir, path, ssid):

        self.directory = os.getcwd() + '/s3_files/' + ssid #path to 'new' file s3_files(master_dir) and another file within that is the ssid file
        self.input_dir = self.directory + '/Input/' #path to '/Input' file within the ssid file
        self.nitro_heatmaps_dir = self.directory + '/Nitro_Heatmaps/' #path to '/Nitro_Heatmaps' file within the ssid file
        self.zip_input_dir = path + master_dir #path to input zip inside of s3_files
        self.zip_output_dir = path + '/s3_zip/' #path to zip located where the code is
        
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        if not os.path.exists(self.input_dir):
            os.makedirs(self.input_dir)
        if not os.path.exists(self.nitro_heatmaps_dir):
            os.makedirs(self.nitro_heatmaps_dir)

    def zipEverything(self):
        shutil.make_archive(self.zip_output_dir, 'zip', self.zip_input_dir)


    