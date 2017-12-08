class Train:
	def __init__(self, trip):
		self.trip = trip
		self.collected_data = {} # Hash: section_id -> timestamp
		self.arrivals = [] # List of [arrival time, stop id]
		self.departures = [] # List of [departure time, stop id]
		self.on_section = [] # List of [departure pair, arrival pair] from above
		self.initialize_events()

	def initialize_events(self):
		stops = [stop_time.stop_sequence
							for stop_time in self.trip.stop_times]
		stops.sort()

		length = len(stops)
		self.arrivals = list(range(length -1))
		self.departures = list(range(length - 1))
		self.on_section = list(range(length - 2))

		# temporary dictionary to speed up lookup
		stop_time_by_seq = {t.stop_sequence: t for t in self.trip.stop_times}

		# TODO: deduplicate the following two code blocks
		# TODO: I feel this can be optimized

		seq = stops[0]
		stop_time = stop_time_by_seq[seq]
		self.arrivals[0] = [stop_time.arrival_time, int(stop_time.stop_id)]
		self.departures[0] = [stop_time.departure_time, int(stop_time.stop_id)]

		for i in range(1, len(stops) - 1):
			seq = stops[i]
			stop_time = stop_time_by_seq[seq]
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
