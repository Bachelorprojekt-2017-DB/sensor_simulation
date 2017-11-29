import os
import sys
import pygtfs
import time
import datetime
import pickle
from functools import reduce
from enum import Enum
from util.graph import Graph
from train import Train

class EventTypes(Enum):
	UNDEFINED = 0
	ARRIVAL = 1
	DEPARTURE = 2
	NOTIFY_ON_SECTION = 3
	ON_SECTION = 4

class Event:
	def __init__(self, iteration, sender, receiver):
		self.iteration = iteration
		self.sender = sender
		self.receiver = receiver

	def call(self):
		self.sender.notify(self.receiver, self.iteration)
		print('sender; {}, receiver: {}'.format(self.sender.collected_data, self.receiver.collected_data))

class Simulation:

	def __init__(self):
		self.gtfs_path = os.path.join(os.path.dirname(__file__), '..', 'data')
		self.graph_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'graph_cache')
		self.trains_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'trains_cache')
		self.time_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'time_cache')
		self.events_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'events_cache')
		self.trains = []
		self.earliest_time = datetime.timedelta.max
		self.latest_time = datetime.timedelta.min

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
				pickle.dump((self.earliest_time, self.latest_time), open(self.time_path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
				stops = sorted(stops, key = lambda x : (x[0]))
				for i in range(0, len(stops) - 2):
					self.graph.get_or_create_section(stops[i][1], stops[i+1][1])


	def create_stations(self, stops):
			for stop in stops:
				self.graph.get_or_create_station(stop.stop_id, stop.stop_name)

	def load_graph(self):
		print('Found previous graph at ', self.graph_path)
		self.graph = pickle.load(open(self.graph_path, 'rb'))
		print('\nStations: {}, Sections: {}'.format(len(self.graph.stations), len(self.graph.sections)))

	def create_graph(self, schedule):
		self.graph = Graph()
		self.create_stations(schedule.stops)
		self.create_sections(schedule)
		pickle.dump(self.graph, open(self.graph_path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
		print('\nStations: {}, Sections: {}'.format(len(self.graph.stations), len(self.graph.sections)))

	def create_trains_from_trips(self, schedule):
		for routes in schedule.routes:
			for trip in routes.trips:
				self.trains.append(Train(trip))
		pickle.dump(self.trains, open(self.trains_path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

	def load_trains(self):
		print('Found previous trains at ', self.trains_path)
		self.trains = pickle.load(open(self.trains_path, 'rb'))

	def create_event(self, time, sender, receiver):
		iteration = self.time_to_iteration(time)
		if iteration < 0:
			return None
		event = Event(iteration, sender, receiver)
		self.event_queue[iteration].append(event)

	def find_station(self, name):
		for station in self.graph.stations:
			if station.stop_name == name:
				return station
		return None

	def print_progress(self, station, time):
		d = len(station.collected_data.keys()) # amount of data at destination station
		o = len(self.graph.sections) # overall amount of data
		n = station.stop_name # name of destination station
		sys.stdout.write('\r {} of {} section information has/have reached {} after {} min, collected: '.format(d, o, n, time, station.collected_data))
		sys.stdout.flush()

	def load_event_queue(self):
		print('Found previous trains at ', self.events_path)
		self.event_queue = pickle.load(open(self.events_path, 'rb'))

	def create_event_queue(self):
		total_iterations = self.time_to_iteration(self.latest_time) # iterations = minutes
		print("Simulation will have {} steps".format(total_iterations))
		self.event_queue = [[] for n in range(total_iterations)]

		for train in self.trains:
			if train == None:
				print('None')
				continue
			for arrival in train.arrivals:
				station = self.graph.get_or_create_station(arrival[1])
				self.create_event(arrival[0], train, station)
			for departure in train.departures:
				station = self.graph.get_or_create_station(departure[1])
				self.create_event(departure[0], station, train)
			for on_section in train.on_section:
				section = self.graph.get_or_create_section(on_section[0][1], on_section[1][1])
				time = on_section[0][0] + datetime.timedelta(minutes = 1)
				self.create_event(time, train, section)
				self.create_event(time, section, train)
			if train == None:
				print('None2')
		pickle.dump(self.event_queue, open(self.events_path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

	def run_event_queue(self):
		destination_station = None

		while destination_station == None:
			# destination = input("Please enter data destination station (x for abort): ")
			destination = 'Frankfurt(Main)Hbf'
			if destination == "x":
				print('Simulation aborted')
				return
			destination_station = self.find_station(destination)
			print(destination_station)

		for event_list in self.event_queue:
			if event_list == []:
				continue
			time = event_list[0].iteration
			for event in event_list:
				event.call()
			self.print_progress(destination_station, time)

	def main(self):

		cache_paths = [self.graph_path, self.trains_path, self.time_path, self.events_path]
		cache_exists = reduce(lambda x,y: x and y, [os.path.isfile(p) for p in cache_paths])

		if(cache_exists):
			print("Skipping data base creation...")

			now = time.time()
			self.load_graph()
			print('Loading Graph object took {} seconds'.format(time.time() - now))

			now = time.time()
			self.load_trains()
			print('Loading Train objects took {} seconds'.format(time.time() - now))

			self.earliest_time, self.latest_time = pickle.load(open(self.time_path, 'rb'))

			now = time.time()
			event_queue = self.load_event_queue()
			print('Loading event queue took {} seconds'.format(time.time() - now))
		else:
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

		now = time.time()
		self.run_event_queue()
		print('Running simulation took {} seconds'.format(time.time() - now))

if __name__ == '__main__':
	Simulation().main()
