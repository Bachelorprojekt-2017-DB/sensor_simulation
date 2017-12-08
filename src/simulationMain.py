import os
import sys
import pygtfs
import time
import datetime
from util.graph import Graph
from util.graph_encoder import GraphEncoder, GraphDecoder
from collections import deque

from train import Train

class Event:
	def __init__(self, iteration, sender, receiver):
		self.iteration = iteration
		self.sender = sender
		self.receiver = receiver

	def call(self):
		self.sender.notify(self.receiver, self.iteration)
		# print('sender; {}, receiver: {}'.format(self.sender.collected_data, self.receiver.collected_data))

class Simulation:
	def __init__(self):
		self.gtfs_path = os.path.join(os.path.dirname(__file__), '..', 'data')
		self.graph_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'graph.json')
		self.database_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database')
		self.trains = deque()
		self.earliest_time = datetime.timedelta.max
		self.latest_time = datetime.timedelta.min

	def time_to_iteration(self, time):
		seconds = (time - self.earliest_time).total_seconds()
		return int(seconds / 60)

	def create_database_from_gtfs(self, path):
		if os.path.isfile(self.database_path):
			schedule = pygtfs.Schedule(self.database_path)
		else:
			schedule = pygtfs.Schedule(self.database_path)
			pygtfs.append_feed(schedule, path)
		return schedule

	def create_sections(self, schedule):
		n = 1
		r = len(schedule.routes)
		for route in schedule.routes:
			sys.stdout.write('\rCreating Graph: Route {} of {}'.format(n, r))
			sys.stdout.flush()
			n += 1
			for trip in route.trips:
				stops = []
				for stop_time in trip.stop_times:
					stops.append([stop_time.stop_sequence, stop_time.stop_id])
				stops = sorted(stops, key = lambda x : (x[0]))
				for i in range(0, len(stops) - 2):
					first_station = self.graph.get_station_by_id(stops[i][1])
					second_station = self.graph.get_station_by_id(stops[i+1][1])
					if not self.graph.section_existing(first_station, second_station):
						self.graph.create_section(first_station, second_station)
		print()


	def create_stations(self, stops):
			for stop in stops:
				if not self.graph.station_existing(stop.stop_id):
					self.graph.create_station(stop.stop_id, stop.stop_name)

	def create_graph(self, schedule):
		if os.path.isfile(self.graph_path):
			self.graph = GraphDecoder().load_from_file(self.graph_path)
		else:
			self.graph = Graph()
			self.create_stations(schedule.stops)
			self.create_sections(schedule)
			GraphEncoder().save_to_file(self.graph, self.graph_path)
		print('Stations: {}, Sections: {}'.format(len(self.graph.stations), len(self.graph.sections)))

	def create_trains_from_trips(self, schedule):
		n = 1
		r = len(schedule.routes)
		for routes in schedule.routes:
			for trip in routes.trips:
				sys.stdout.write('\rCreating Trains: Route {} of {}'.format(n, r))
				sys.stdout.flush()
				self.trains.append(Train(trip))
				for stop_time in trip.stop_times:
					if self.earliest_time > stop_time.arrival_time:
						self.earliest_time = stop_time.arrival_time
					if self.latest_time < stop_time.departure_time:
						self.latest_time = stop_time.departure_time
			n += 1
		print()

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

	def create_event_queue(self):
		total_iterations = self.time_to_iteration(self.latest_time) # iterations = minutes
		print("Simulation will have {} steps".format(total_iterations))
		self.event_queue = [[] for n in range(total_iterations)]

		# TODO: get rid of O(n) lookups (``graph.get_station_by_id``)

		for train in self.trains:
			if train == None:
				continue
			for arrival in train.arrivals:
				station = self.graph.get_station_by_id(arrival[1])
				self.create_event(arrival[0], train, station)
			for departure in train.departures:
				station = self.graph.get_station_by_id(departure[1])
				self.create_event(departure[0], station, train)
			for on_section in train.on_section:
				first_station = self.graph.get_station_by_id(on_section[0][1])
				second_station = self.graph.get_station_by_id(on_section[1][1])
				section = self.graph.get_section(first_station, second_station)
				time = on_section[0][0] + datetime.timedelta(minutes = 1)
				self.create_event(time, train, section)
				self.create_event(time, section, train)

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
