import time

# Graph class
# Use getOrCreateStation(stop_id, stop_name) for a single station instance
# Use getOrCreateSection(start_stop_id, end_stop_id) for a single section instance
# Use graph_intance.sections and graph_instance.stations for all of the respective instances

class Graph:
	sections = []
	stations = []
	highest_id = 0

	def getOrCreateStation(self, stop_id, stop_name):
		station = self.station(stop_id)
		if not station.isValid():
			station = _Station(stop_id, stop_name)
			if not station.isValid():
				return station
			self.stations.append(station)
		return station

	def getOrCreateSection(self, start_stop_id, end_stop_id):
		start_station = self.getOrCreatestation(start_stop_id)
		end_station = self.getOrCreatestation(end_stop_id)
		if not (start_station.isValid() and end_station.isValid()):
			return _Section()
		return self._getOrCreateSection(start_station, end_station)

	def _getOrCreateSection(self, first_station, second_station):
		section = self.section(first_station, second_station)
		if not section.isValid():
			section = _Section(self.highest_id, first_station, second_station)
			highest_id += 1
			first_station.addIncident(second_station, section)
			second_station.addIncident(first_station, section)
			self.sections.append(section)
		return section

	def _station(self, stop_id):
		for station in stations:
			if (station.stop_id == stop_id):
				return station
		return _Station()

	def _section(self, first_station, second_station):
		for section in sections:
			if (e.first_station == first_station and e.second_station == second_station or
				e.second_station == first_station and e.first_station == second_station):
				return e
		return Section()

class _TrainLocation:
	current_trains = []

	def add_train(self, train):
		self.current_trains.append(train)

# private Station class for Graph, only instantiate over Graph class
class _Station(_TrainLocation):
	self.collected_data = {} # Hash: section id => timestamp when visited
	self.incidents = {} # Hash: adjacent station id => section id

	def __init__(self, stop_id, stop_name):
		self.stop_id = stop_id
		self.stop_name = stop_name

	def isValid(self):
		return False if (self.stop_id is None) else True

	def addIncident(station, section):
		self.incidents[station] = section

	def informTrains(self):
		for train in self.current_trains:
			train.collected_data = 	self.collected_data

# private Section class for Graph, only instantiate over Graph class
class _Section(_TrainLocation):
data = ""

	def __init__(self, section_id, first_station, second_station):
		self.first_station = first_station
		self.second_station = second_station
		self.section_id = section_id

	def isValid(self):
		return False if (self.first_stop_id is None or self.second_stop_id is None) else True

	def inform_trains(self):
		for train in self.current_trains:
			train.collected_data[section_id] = time.gmtime(time.time()) # TODO: replace with current step