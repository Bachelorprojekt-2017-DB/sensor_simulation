import os
from Data import *
from Graph import *
import random
import time
import pygtfs

DB_NAME = "db_fernstrecke"
schedule = ""
stationsContainingTrains = ""

def setUpDatabase():
	database_location = os.path.join(os.path.dirname(__file__), DB_NAME)
	data_location = os.path.join(os.path.dirname(__file__), "../data")
	
	if(os.path.isfile(database_location)):
		global schedule 
		schedule = pygtfs.Schedule(database_location)
		print("Database detected at", database_location,"\n")
	else:
		global schedule
		schedule = pygtfs.Schedule(database_location)
		pygtfs.append_feed(schedule, data_location)
		print("Created new database at", database_location,"\n")

def parseStations():
	if (schedule is ""):
		print "No schedule existing"
		return
	else:
		return
		
#-------------------------------------------------------------MAIN-------------------------------------------------------------

if __name__ == "__main__":
	setUpDatabase()
	print schedule.stops[0].stop_name
	
	#for t in range (0, 2400):
		