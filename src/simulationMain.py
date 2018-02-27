import os
import sys
import pygtfs
import time
import datetime
from graph import Graph

class Event:
	def __init__(self, iteration, sender, receiver):
		self.iteration = iteration
		self.sender = sender
		self.receiver = receiver

	def call(self):
		self.sender.notify(self.receiver, self.iteration)
		# print('sender; {}, receiver: {}'.format(self.sender.collected_data, self.receiver.collected_data))

class Train:
	def __init__(self, trip):
		self.trip = trip
		self.collected_data = {} # Hash: section_id -> timestamp
		self.arrivals = [] # List of [arrival time, stop id]
		self.departures = [] # List of [departure time, stop id]
		self.on_section = [] # List of [departure pair, arrival pair] from above
		self.initialize_events()

	def stop_time_by_seq(self, seq):
		for stop_time in self.trip.stop_times:
			if stop_time.stop_sequence == seq:
				return stop_time

	def initialize_events(self):
		stops = []
		for stop_time in self.trip.stop_times:
			stops.append(stop_time.stop_sequence)
		stops.sort()

		length = len(stops)
		self.arrivals = list(range(length -1))
		self.departures = list(range(length - 1))
		self.on_section = list(range(length - 2))

		seq = stops[0]
		stop_time = self.stop_time_by_seq(seq)
		self.arrivals[0] = [stop_time.arrival_time, int(stop_time.stop_id)]
		self.departures[0] = [stop_time.departure_time, int(stop_time.stop_id)]

		for i in range(1, len(stops) - 1):
			seq = stops[i]
			stop_time = self.stop_time_by_seq(seq)
			self.arrivals[i] = [stop_time.arrival_time, int(stop_time.stop_id)]
			self.departures[i] = [stop_time.departure_time, int(stop_time.stop_id)]
			self.on_section[i-1] = [self.departures[i - 1], self.arrivals[i]]

	def notify(self, train_location, time):
		train_location.update(self.collected_data)

	def update(self, data):
		for i in data:
			if data[i] == None:
				continue
			elif self.collected_data.get(i, 0) < data[i]:
				self.collected_data[i] = data[i]

class Simulation:
	def __init__(self):
		self.gtfs_path = os.path.join(os.path.dirname(__file__), '..', 'data')
		self.graph_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'graph.json')
		self.database_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'database')
		self.trains = []
		self.earliest_time = datetime.timedelta.max
		self.latest_time = datetime.timedelta.min
		self.schedule = []

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
					stop_id = int(stop_time.stop_id)
					stops.append([stop_time.stop_sequence, stop_id])
				stops = sorted(stops, key = lambda x : (x[0]))
				for i in range(0, len(stops) - 2):
					first_station = self.graph.get_station_by_id(stops[i][1])
					second_station = self.graph.get_station_by_id(stops[i+1][1])
					if not self.graph.section_existing(first_station, second_station):
						self.graph.create_section(first_station, second_station)
		print()


	def create_stations(self, stops):
			for stop in stops:
				stop_id = int(stop.stop_id)
				if not self.graph.station_existing(stop_id):
					self.graph.create_station(stop_id, stop.stop_name)

	def create_graph(self, schedule):
		# if os.path.isfile(self.graph_path):
		if False:
			self.graph = GraphDecoder().load_from_file(self.graph_path)
		else:
			self.graph = Graph()
			self.create_stations(schedule.stops)
			self.create_sections(schedule)
			# GraphEncoder().save_to_file(self.graph, self.graph_path)
		print('Stations: {}, Sections: {}'.format(len(self.graph.stations), len(self.graph.sections)))

	def create_trains_from_trips(self, schedule):
		n = 1
		r = len(schedule.routes)
		for routes in schedule.routes:
			for trip in routes.trips:
				sys.stdout.write('\rCreating Trains: Route {} of {}'.format(n, r))
				sys.stdout.flush()
				if len(trip.stop_times) < 2:
					continue
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
		start_date = datetime.date(2017, 1, 1)
		self.earliest_time = start_date
		end_date = datetime.date(2017, 2, 1)
		self.latest_time = end_date

		total_iterations = self.time_to_iteration(end_date + datetime.timedelta(days=2)) # add one more day to be sure
		print("Simulation will have {} steps".format(total_iterations))
		self.event_queue = [[] for n in range(total_iterations)]

		while(start_date <= end_date):
			self.create_day_event_queue(start_date)
			start_date += datetime.timedelta(days=1)

	def create_day_event_queue(self, date):
		active_services = self.schedule.session.query(pygtfs.gtfs_entities.ServiceException).filter(pygtfs.gtfs_entities.ServiceException.date == date).all()
		active_services_ids = [x.id for x in active_services]
		trains_on_day = [x for x in self.trains if x.trip.service_id in active_services_ids]

		for train in trains_on_day:
			if train == None:
				continue
			for arrival in train.arrivals:
				station = self.graph.get_station_by_id(arrival[1])
				self.create_event(arrival[0] + date, train, station)
			for departure in train.departures:
				station = self.graph.get_station_by_id(departure[1])
				self.create_event(departure[0] + date, station, train)
			for on_section in train.on_section:
				first_station = self.graph.get_station_by_id(on_section[0][1])
				second_station = self.graph.get_station_by_id(on_section[1][1])
				section = self.graph.get_section(first_station, second_station)
				time = on_section[0][0] + datetime.timedelta(minutes = 1) + date
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
		self.print_progress(destination_station,self.latest_time)

		graph_sections = set([x.section_id for x in self.graph.sections])
		collected_sections = []
		for key,val in destination_station.collected_data.items():
			collected_sections.append(key)
		collected_sections = set(collected_sections)

		missing_sections = graph_sections - collected_sections
		missing_sections = list(missing_sections)
		for s in self.graph.sections:
			if s.section_id in missing_sections:
				print(s.first_station.stop_name, ' -- ', s.second_station.stop_name)

	def main(self):
		# setup simulation from gtfs file
		now = time.time()
		self.schedule = self.create_database_from_gtfs(self.gtfs_path)
		print('Creating Database took {} seconds'.format(time.time() - now))

		now = time.time()
		self.create_graph(self.schedule)
		print('Creating Graph object took {} seconds'.format(time.time() - now))

		now = time.time()
		self.create_trains_from_trips(self.schedule)
		print('Creating Train objects took {} seconds'.format(time.time() - now))

		now = time.time()
		event_queue = self.create_event_queue()
		print('Creating event queue took {} seconds'.format(time.time() - now))

		now = time.time()
		self.run_event_queue()
		print('Running simulation took {} seconds'.format(time.time() - now))

if __name__ == '__main__':
	Simulation().main()
