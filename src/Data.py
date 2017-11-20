import time
import os

class RailwaySectionInformation:
	
	timestamp = time.gmtime(0)
	data = ""
	sectionId = -1
	
	def __init__(self, sectionId, timestamp, info):
		self.sectionId = sectionId
		self.timestamp = time.gmtime(timestamp)
		self.information = info
		
class Train:
	
	collectedData = {}
	trip = ""
	
	def __init__(self, trip):
		self.trip = trip