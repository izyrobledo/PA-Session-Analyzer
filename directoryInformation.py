class dirAndUserInfo:



	master_dir = ''
	path = ''
	ssid = ''
	directory = ''
	input_dir = ''
	nitro_heatmaps_dir = ''
	zip_input_dir = ''
	zip_output_dir = ''


	def __init__(self, master_dir, path, ssid):
		self.master_dir = '/s3_files/'
		directory = path + master_dir + ssid #path to 'new' file s3_files(master_dir) and another file within that is the ssid file
	    input_dir = directory + '/Input/' #path to '/Input' file within the ssid file
	    nitro_heatmaps_dir = directory + '/Nitro_Heatmaps/' #path to '/Nitro_Heatmaps' file within the ssid file
	    zip_input_dir = path + master_dir #path to input zip inside of s3_files

	    zip_output_dir = path + '/s3_zip/' #path to zip located where the code is


	def makeDirs():
	    if not os.path.exists(directory):
	      os.makedirs(directory)
	    if not os.path.exists(input_dir):
	      os.makedirs(input_dir)
	    if not os.path.exists(nitro_heatmaps_dir):
	      os.makedirs(nitro_heatmaps_dir)
