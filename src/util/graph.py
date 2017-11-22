import time

# Graph class
# Use get_or_create_station(stop_id, stop_name) for a single station instance
# Use get_or_create_section(start_stop_id, end_stop_id) for a single section instance
# Use graph_intance.sections and graph_instance.stations for all of the respective instances

class Graph:
	sections = []
	stations = []
	highest_id = 0

	def get_section_by_id(self, section_id):
		for section in self.sections:
			if section.section_id == section_id:
				return section
		return _Section()

	def get_station_by_id(self, station_id):
		for station in self.stations:
			if station.stop_id == station_id:
				return station
		return _Station()		

	def get_or_create_station(self, stop_id, stop_name = ''):
		station = self._station(stop_id)
		if not station.is_valid():
			station = _Station(stop_id, stop_name)
			if not station.is_valid():
				return station
			self.stations.append(station)
		return station

	def get_or_create_section(self, start_stop_id, end_stop_id):
		start_station = self.get_or_create_station(start_stop_id)
		end_station = self.get_or_create_station(end_stop_id)
		if not (start_station.is_valid() and end_station.is_valid()):
			return _Section()
		return self._get_or_create_section(start_station, end_station)

	def _get_or_create_section(self, first_station, second_station):
		section = self._section(first_station, second_station)
		if not section.is_valid():
			section = _Section(self.highest_id, first_station, second_station)
			self.highest_id += 1
			first_station.add_incident(second_station, section)
			second_station.add_incident(first_station, section)
			self.sections.append(section)
		return section

	def _station(self, stop_id):
		for station in self.stations:
			if (station.stop_id == stop_id):
				return station
		return _Station()

	def _section(self, first_station, second_station):
		for section in self.sections:
			if (section.first_station == first_station and section.second_station == second_station or
				section.second_station == first_station and section.first_station == second_station):
				return section
		return _Section()

# private Station class for Graph, only instantiate over Graph class
class _Station():
	collected_data = [] # List: section id => timestamp when visited
	incidents = {} # Hash: adjacent station id => section id

	def __init__(self, stop_id = None, stop_name = None):
		self.stop_id = stop_id
		self.stop_name = stop_name

	def is_valid(self):
		return False if (self.stop_id is None) else True

	def add_incident(self, station, section):
		self.incidents[station] = section

	def notify(self, train, time):
		train.update(self.collected_data)

	def update(self, data):
		for i in range(len(data) - 1):
			if data[i] == None:
				continue
			elif self.collected_data[i] < data[i]:
				self.collected_data[i] = data[i] 

	def __str__(self):
		return 'Station {}: {}'.format(self.stop_id, self.stop_name)

# private Section class for Graph, only instantiate over Graph class
class _Section():
	def __init__(self, section_id = None, first_station = None, second_station = None):
		self.first_station = first_station
		self.second_station = second_station
		self.section_id = section_id

	def is_valid(self):
		return False if (self.first_station is None or self.second_station is None) else True

	def notify(self, train, iteration):
		train.update([self.section_id], iteration)

	def update(self, data):
		pass

	def __str__(self):
		return 'Section {}: {}, {}'.format(self.section_id, self.first_station, self.second_station)