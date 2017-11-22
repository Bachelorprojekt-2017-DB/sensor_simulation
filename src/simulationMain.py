import os
import sys
import pygtfs
import time
import datetime
from enum import Enum
from util.graph import Graph
from train import Train

class EventTypes(Enum):
	UNDEFINED = 0
	ARRIVAL = 1
	DEPARTUE = 2
	NOTIFY_ON_SECTION = 3
	ON_SECTION = 4

class Event:
	sender = None # possible actors should be Train, _Station or _Section objects
	receiver = None # Used when Train informs station/section of arrival on that station/section
	iteration = -1
	event_type = EventTypes.UNDEFINED

	def __init__(self, event_type, iteration, sender, receiver = None):
		self.event_type = event_type
		self.iteration = iteration
		self.sender = sender
		self.receiver = receiver

class Simulation:
	gtfs_path = os.path.join(os.path.dirname(__file__), '..', 'data')
	trains = []
	earliest_time = datetime.timedelta.max
	latest_time = datetime.timedelta.min

	def time_to_iteration(self, time):
		seconds = (time - self.earliest_time).total_seconds()
		return int(seconds / 60)

	def create_database_from_gtfs(self, path):
		schedule = pygtfs.Schedule(':memory:') # in-memory database, can also be written to a file
		pygtfs.append_feed(schedule, path)
		return schedule

	def create_sections(self, schedule):
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
					if self.earliest_time > stop_time.arrival_time:
						self.earliest_time = stop_time.arrival_time
					if self.latest_time < stop_time.departure_time:
						self.latest_time = stop_time.departure_time
				stops = sorted(stops, key = lambda x : (x[0]))
				for i in range(0, len(stops) - 2):
					self.graph.get_or_create_section(stops[i][1], stops[i+1][1])


	def create_stations(self, stops):
			for stop in stops:
				self.graph.get_or_create_station(stop.stop_id)

	def create_graph(self, schedule):
		self.graph = Graph()
		self.create_stations(schedule.stops)
		self.create_sections(schedule)
		print('\nStations: {}, Sections: {}'.format(len(self.graph.stations), len(self.graph.sections)))

	def create_trains_from_trips(self, schedule):
		for routes in schedule.routes:
			for trip in routes.trips:
				self.trains.append(Train(trip))

	def create_event(self, event_type, time, train_location_id, train = None):
		iteration = self.time_to_iteration(time)
		if iteration < 0:
			return None
		if event_type == EventTypes.ARRIVAL:
			if train == None:
				return None
			actor = train
		elif event_type == EventTypes.DEPARTUE:
			actor = self.graph.get_or_create_station(train_location_id)
		elif event_type == EventTypes.ON_SECTION:
			actor = self.graph.get_or_create_section(train_location_id)
		else:
			return None
		event = Event(event_type, time, actor)
		self.event_queue[iteration].append(event)

	def create_event_queue(self):
		total_iterations = self.time_to_iteration(self.latest_time) # iterations = minutes
		print("Simulation will have {} steps".format(total_iterations))
		self.event_queue = [[] for n in range(total_iterations)]
		for i in range(len(self.trains)):
			train = self.trains[i]
			for i in range(len(train.arrivals)):
				arrival = train.arrivals[i]
				print(arrival)
				station = self.graph.get_or_create_station(arrival[1])
				self.create_event(EventTypes.ARRIVAL, arrival[0], train, station)
			for departure in train.departures:
				station = self.graph.get_or_create_station(departure[1])
				self.create_event(EventTypes.DEPARTUE, departure[0], station)
			for section in train.on_section:
				sectiond = self.graph.get_or_create_section(section[0][1], section[1][1])
				time = section[0][0] + datetime.timedelta(minutes = 1)
				self.create_event(EventTypes.NOTIFY_ON_SECTION, time, train, section)
				self.create_event(EventTypes.ON_SECTION, time, section)

	def main(self):
		# setup simulation from gtfs file
		now = time.time()
		schedule = self.create_database_from_gtfs(self.gtfs_path)
		print('Creating Database took {} seconds'.format(time.time() - now))

		now = time.time()
		self.create_graph(schedule)
		print('Creating Graph object took {} seconds'.format(time.time() - now))

		now = time.time()
		self.create_trains_from_trips(schedule)
		print('Creating Train objects took {} seconds'.format(time.time() - now))

		now = time.time()
		event_queue = self.create_event_queue()
		print('Creating event queue took {} seconds'.format(time.time() - now))

if __name__ == '__main__':
	Simulation().main()