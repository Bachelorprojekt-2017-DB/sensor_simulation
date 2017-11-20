import time
from Data import RailwaySectionInformation, Train

class TrainLocation:
	
	currentTrains = []

class Station(TrainLocation):
	
	collectedData = {}
	stationId = -1
	
	def __init__(self, stationId):
		self.stationId = stationId
		
	def addTrain(self, train):
		self.currentTrains.append(train)
		
	def informTrains(self):
		for t in currentTrains:
			t.collectedData = self.collectedData
		
class RailwaySection(TrainLocation):
	
	data = ""
	sectionId = -1
	firstStation = ""
	secondStation = ""
	
	def __init__(self, sectionId):
		self.sectionId = sectionId
		
	def updateData(self):
		data = RailwaySectionInformation(self.sectionId, time.time(), "whatever")
		
	def addTrain(self, train):
		self.currentTrains.append(train)	
		
	def informTrains(self):
		self.updateData()
		for t in currentTrains:
			t.collectedData[sectionId] = data		
		
#str(self.timestamp.tm_hour) + ":" + str(self.timestamp.tm_min) + " " + str(self.timestamp.tm_mday) + "/" + str(self.timestamp.tm_mon) + "/" + str(self.timestamp.tm_year)