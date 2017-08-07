class AWSEnvironment:
	session_list = ['']
	session_table = ''
	s3_image_bucket = ''
	s3_heatmap_bucket = ''
	region_name = ''


	def __init__(self, session_table, s3_image_bucket, s3_heatmap_bucket, region_name):
		
		self.session_table = session_table
		self.s3_image_bucket = s3_image_bucket
		self.s3_heatmap_bucket = s3_heatmap_bucket
		self.region_name = region_name

	def listSSIDInfo(self, session_list):
		self.session_list = session_list
	# more stuff

	