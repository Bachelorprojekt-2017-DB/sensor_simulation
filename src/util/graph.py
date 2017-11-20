# Graph class
# Use getOrCreateStation(stop_id, stop_name) for stations
# Use getOrCreateEdge(start_stop_id, end_stop_id) for sections

class Graph:
	def __init__(self):
		self.sections = []
		self.stations = []
		self.highest_id = 0

	def getOrCreateStation(stop_id, stop_name):
		station = self.station(stop_id)
		if not station.isValid():
			station = _Station(stop_id, stop_name)
			if not station.isValid():
				return station
			self.stations.append(station)
		return station

	def getOrCreateSection(start_stop_id, end_stop_id):
		start_station = self.getOrCreatestation(start_stop_id)
		end_station = self.getOrCreatestation(end_stop_id)
		if not (start_station.isValid() and end_station.isValid()):
			return _Section()
		return self._getOrCreateSection(start_station, end_station)

	def _getOrCreateSection(first_station, second_station):
		section = self.section(first_station, second_station)
		if not section.isValid():
			section = _Section(self.highest_id, first_station, second_station)
			highest_id += 1
			first_station.addIncident(second_station, section)
			second_station.addIncident(first_station, section)
			self.sections.append(section)
		return section

	def _station(stop_id):
		for station in stations:
			if (station.stop_id == stop_id):
				return station
		return _Station()

	def _section(first_station, second_station):
		for section in sections:
			if (e.first_station == first_station and e.second_station == second_station or
				e.second_station == first_station and e.first_station == second_station):
				return e
		return Edge()

# private Station class for Graph, only instantiate over Graph class
class _Station:
	def __init__(self, stop_id, stop_name):
		self.stop_id = stop_id
		self.stop_name = stop_name
		self.collected_data = {} # Hash: section id => timestamp when visited
		self.incidents = {} # Hash: adjacent station id => section id

	def isValid():
		return False if (self.stop_id is None) else True

	def addIncident(station, section):
		self.incidents[station] = section

# private Edge class for Graph, only instantiate over Graph class
class _Section:
	def __init__(self, section_id, first_station, second_station):
		self.first_station = first_station
		self.second_station = second_station
		self.section_id = section_id

	def isValid():
		return False if (self.first_stop_id is None or self.second_stop_id is None) else True