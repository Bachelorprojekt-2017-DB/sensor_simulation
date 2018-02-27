import datetime

class Graph:
	def __init__(self):
		self.stations = []
		self.sections = []
		self.highest_id = 0

	def station_existing(self, stop_id_or_name):
		for station in self.stations:
			if isinstance(stop_id_or_name, int):
				if station.stop_id == stop_id_or_name:
					return True
			if isinstance(stop_id_or_name, str):
				if station.stop_name == stop_id_or_name:
					return True
		return False

	def get_station_by_id(self, stop_id):
		for station in self.stations:
			if station.stop_id == stop_id:
				return station
		raise ValueError('No station found with id {}'.format(stop_id))

	def get_station_by_name(self, stop_name):
		for station in self.stations:
			if station.stop_name == stop_name:
				return station
		raise ValueError('No station found with name {}'.format(stop_name))

	def create_station(self, stop_id, stop_name):
		if self.station_existing(stop_id):
			station = self.get_station_by_id(stop_id)
			raise ValueError('{} already existing'.format(station))
		if self.station_existing(stop_name):
			station = self.get_station_by_name(stop_name)
			raise ValueError('{} already existing'.format(station))
		station = Station(stop_id, stop_name)
		self.stations.append(station)

	def section_existing(self, first_station, second_station):
		for section in self.sections:
			if ((section.first_station == first_station and section.second_station == second_station) or (section.second_station == first_station and section.first_station == second_station)):
				return True
		return False

	def get_section(self, first_station, second_station):
		for section in self.sections:
			if ((section.first_station == first_station and section.second_station == second_station) or (section.second_station == first_station and section.first_station == second_station)):
				return section
		raise ValueError('No section found with {} and {}'.format(first_station, second_station))

	def create_section(self, first_station, second_station):
		if self.section_existing(first_station, second_station):
			section = self.get_section(first_station, second_station)
			raise ValueError('{} already existing'.format(section))
		section = Section(self.highest_id, first_station, second_station)
		self.sections.append(section)
		self.highest_id += 1

	def isEmpty(self):
		return not (self.stations or self.sections)

class Station:
	def __init__(self, stop_id, stop_name):
		if not isinstance(stop_id, int):
			raise TypeError('Station: stop_id is not an int it is ', type(stop_id), ' value: ', str(stop_id))
		if not isinstance(stop_name, str):
			raise TypeError('Station: stop_name is not a string')
		self.stop_id = stop_id
		self.stop_name = stop_name
		self.collected_data = {}

	def notify(self, train, time):
		train.update(self.collected_data)

	def update(self, data):
		for i in data:
			if data[i] == None:
				continue
			elif self.collected_data.get(i, 0) < data[i]:
				self.collected_data[i] = data[i]

	def isValid(self):
		return (isinstance(self.stop_id, int) and isinstance(self.stop_name, str) and (self.stop_id >= 0) and (self.stop_name))

	def __str__(self):
		return 'Station {}: {}'.format(self.stop_id, self.stop_name)

class Section:
	def __init__(self, section_id, first_station, second_station):
		if not isinstance(section_id, int):
			raise TypeError('Section: section id is not an int')
		if not isinstance(first_station, Station):
			raise TypeError('Section: first_station is not a Station object')
		if not isinstance(second_station, Station):
			raise TypeError('Section: second_station is not a Station object')
		self.section_id = section_id
		self.first_station = first_station
		self.second_station = second_station
		self.collected_data = {}
		self.collected_data[section_id] = datetime.timedelta.min

	def notify(self, train, time):
		self.collected_data[self.section_id] = time
		train.update(self.collected_data)

	def update(self, data):
		pass

	def isValid(self):
		return (isinstance(self.section_id, int) and isinstance(self.first_station, Station) and isinstance(self.second_station, Station) and self.section_id >= 0 and self.first_station.isValid() and self.second_station.isValid())

	def __str__(self):
		return 'Section {}: {}, {}'.format(self.section_id, self.first_station, self.second_station)
