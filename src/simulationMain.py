import os
import sys
import pygtfs
import time
from util.graph import Graph
from train import Train

class Simulation:
	gtfs_path = os.path.join(os.path.dirname(__file__), '..', 'data')
	trains = []

	def create_database_from_gtfs(self, path):
		schedule = pygtfs.Schedule(':memory:') # in-memory database, can also be written to a file
		pygtfs.append_feed(schedule, path)
		return schedule

	def create_sections(self, graph, schedule):
		n = 1
		r = len(schedule.routes)
		for route in schedule.routes:
			sys.stdout.write('\rRoute {} from {}'.format(n, r))
			sys.stdout.flush()
			n += 1
			for trip in route.trips:
				stops = []
				for stop_time in trip.stop_times:
					stops.append([stop_time.stop_sequence, stop_time.stop_id])
				stops = sorted(stops, key = lambda x : (x[0]))
				for i in range(0, len(stops) - 2):
					graph.get_or_create_section(stops[i][1], stops[i+1][1])


	def create_stations(self, graph, stops):
			for stop in stops:
				graph.get_or_create_station(stop.stop_id)

	def create_graph(self, schedule):
		graph = Graph()
		self.create_stations(graph, schedule.stops)
		self.create_sections(graph, schedule)
		print('\nStations: {}, Sections: {}'.format(len(graph.stations), len(graph.sections)))
		return graph

	def create_trains_from_trips(self, schedule):
		for routes in schedule.routes:
			for trip in routes.trips:
				self.trains.append(Train(trip))

	def create_event_queue(self):
		print('TODO')

	def main(self):
		# setup simulation from gtfs file
		now = time.time()
		schedule = self.create_database_from_gtfs(self.gtfs_path)
		print('Creating Database took {} seconds'.format(time.time() - now))
		now = time.time()
		graph = self.create_graph(schedule)
		print('Creating Graph object took {} seconds'.format(time.time() - now))
		now = time.time()
		self.trains = self.create_trains_from_trips(schedule)
		print('Creating Train objects took {} seconds'.format(time.time() - now))
		now = time.time()
		event_queue = self.create_event_queue()
		print('Creating event queue took {} seconds'.format(time.time() - now))


	# def prepareEventQueue():
	# 	twoDayTrips = set()
	# 	stops = schedule.stop_times
		
	# 	for st in stops:
	# 		arrTime = str (st.arrival_time)
	# 		arrTime = arrTime[:len(arrTime) - 3].replace(":","")
			
	# 		if (isNoNumber(arrTime)):
	# 			twoDayTrips.add(st.trip_id)
		
	# 	cleanStops = set()
		
	# 	for st in stops:
	# 		if (st.trip_id not in twoDayTrips):
	# 			cleanStops.add(st)
				
	# 	for st in cleanStops:
	# 		key = str (st.arrival_time)
	# 		key = key[:len(key) - 3].replace(":","")
			
	# 		if key in eventQueue:
	# 			eventQueue[key].append(st)
	# 		else:
	# 			eventQueue[key] = [st]

if __name__ == '__main__':
	Simulation().main()