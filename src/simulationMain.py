import os
import sys
import pygtfs
import time
from util.graph import Graph

class Simulation:
	gtfs_path = os.path.join(os.path.dirname(__file__), "..", "data")

	def createDatabaseFromGTFS(self, path):
		schedule = pygtfs.Schedule(":memory:") # in-memory database, can also be written to a file
		pygtfs.append_feed(schedule, path)
		return schedule

	def createSections(self, graph, schedule):
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
					graph.getOrCreateSection(stops[i][1], stops[i+1][1])


	def createStations(self, graph, stops):
			for stop in stops:
				graph.getOrCreateStation(stop.stop_id)

	def createGraph(self, schedule):
		graph = Graph()
		self.createStations(graph, schedule.stops)
		self.createSections(graph, schedule)
		print('\nStations: {}, Sections: {}'.format(len(graph.stations), len(graph.sections)))
		return graph

	def createTrainsFromTrips(self, schedule):
		print('Todo')

	def main(self):
		# setup simulation from gtfs file
		now = time.time()
		schedule = self.createDatabaseFromGTFS(self.gtfs_path)
		print('Creating Database took {} seconds'.format(time.time() - now))
		now = time.time()
		graph = self.createGraph(schedule)
		print('Creating Graph took {} seconds'.format(time.time() - now))
		trains = self.createTrainsFromTrips(schedule)

if __name__ == "__main__":
	Simulation().main()
