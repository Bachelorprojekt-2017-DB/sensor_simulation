import os
import sys
from Data import *
from Graph import *
import random
import time
import pygtfs

sys.path.insert(0, 'util')

from graph import Graph

DB_NAME = "db_fernstrecke"
schedule = ""
stationsContainingTrains = ""
eventQueue = dict()
trains = dict()
trafficNetwork = ""
sortedTrips = {}

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

def isNoNumber(s):
    try:
        int(s)
        return False
    except ValueError:
        return True
	
def prepareEventQueue():
	twoDayTrips = set()
	
	stops = schedule.stop_times
	
	for st in stops:
		arrTime = str (st.arrival_time)
		arrTime = arrTime[:len(arrTime) - 3].replace(":","")
		
		if (isNoNumber(arrTime)):
			twoDayTrips.add(st.trip_id)
	
	cleanStops = set()
	
	for st in stops:
		if (st.trip_id not in twoDayTrips):
			cleanStops.add(st)
			
	for st in cleanStops:
		key = str (st.arrival_time)
		key = key[:len(key) - 3].replace(":","")
		
		if key in eventQueue:
			eventQueue[key].append(st)
		else:
			eventQueue[key] = [st]
			
def initializeTrainsAndTrips():
	for t in schedule.trips:
		trains[t.trip_id] = Train(t)
		
def setUpGraph():
	trafficNetwork = Graph()
	
	for s in schedule.stops:
		trafficNetwork.get_or_create_vertex(s.stop_id, s.stop_name)
	
	
#-------------------------------------------------------------MAIN-------------------------------------------------------------

if __name__ == "__main__":
	setUpDatabase()
	prepareEventQueue()
	initializeTrains()
	
	print "simulation finished"