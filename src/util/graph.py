import datetime

class Graph:
	def __init__(self):
		self.stations = {} # stop_id -> station
		self.sections = []
		self.highest_id = 0

	def station_existing(self, stop_id):
		return stop_id in self.stations

	def get_station_by_id(self, stop_id):
		return self.stations[stop_id]

	def create_station(self, stop_id, stop_name):
		if stop_id in self.stations:
			station = self.get_station_by_id(stop_id)
			raise Exception('{} already existing'.format(station))
		self.stations[stop_id] = Station(stop_id, stop_name)

	def section_existing(self, first_station, second_station):
		for section in self.sections:
			if ((section.first_station == first_station and section.second_station == second_station) or (section.second_station == first_station and section.first_station == second_station)):
				return True
		return False

	def get_section(self, first_station, second_station):
		for section in self.sections:
			if ((section.first_station == first_station and section.second_station == second_station) or (section.second_station == first_station and section.first_station == second_station)):
				return section
		raise Exception('No section found with {} and {}'.format(first_station, second_station))

	def create_section(self, first_station, second_station):
		if self.section_existing(first_station, second_station):
			section = self.get_section(first_station, second_station)
			raise Exception('{} already existing'.format(section))
		section = Section(self.highest_id, first_station, second_station)
		self.sections.append(section)
		self.highest_id += 1

class Station:
	def __init__(self, stop_id, stop_name):
		self.stop_id = stop_id
		self.stop_name = stop_name
		self.collected_data = {}

	def notify(self, train, time):
		train.update(self.collected_data)

	def update(self, data):
		# TODO: deduplicate with ``Train.update``
		for section_id, timestamp in data.items():
			if timestamp is None:
				continue
			if self.collected_data.get(section_id, 0) < timestamp:
				self.collected_data[section_id] = timestamp

	def __str__(self):
		return 'Station {}: {}'.format(self.stop_id, self.stop_name)

class Section:
	def __init__(self, section_id, first_station, second_station):
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

	def __str__(self):
		return 'Section {}: {}, {}'.format(self.section_id, self.first_station, self.second_station)
