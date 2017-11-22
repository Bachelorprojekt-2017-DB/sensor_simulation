class Train:	
	collectedData = {} # Hash: section_id -> timestamp
	arrivals = [] # List of [arrival time, stop id]
	departures = [] # List of [departure time, stop id]
	on_section = [] # List of [departure pair, arrival pair] from above

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
		self.arrivals = list(range(length))
		self.departures = list(range(length))
		self.on_section = list(range(length - 1))

		seq = stops[0]
		stop_time = self.stop_time_by_seq(seq)
		self.arrivals[0] = [stop_time.arrival_time, stop_time.stop_id]
		self.departures[0] = [stop_time.departure_time, stop_time.stop_id]

		for i in range(1, len(stops) - 1):
			seq = stops[i]
			stop_time = self.stop_time_by_seq(seq)
			self.arrivals[i] = [stop_time.arrival_time, stop_time.stop_id]
			self.departures[i] = [stop_time.departure_time, stop_time.stop_id]
			self.on_section[i-1] = [self.departures[i - 1], self.arrivals[i]]

	def __init__(self, trip):
		self.trip = trip
		self.initialize_events()