class Train:	
	collectedData = {} # Hash: section_id -> timestamp
	arrival = [] # List of [arrival time, stop id]
	departure = [] # List of [departure time, stop id]
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
		self.arrival = self.departure = list(range(length))
		self.on_section = list(range(length - 1))

		seq = stops[0]
		stop_time = self.stop_time_by_seq(seq)
		self.arrival[0] = [stop_time.arrival_time, stop_time.stop_id]
		self.departure[0] = [stop_time.departure_time, stop_time.stop_id]

		for i in range(1, len(stops) - 1):
			seq = stops[i]
			stop_time = self.stop_time_by_seq(seq)
			self.arrival[i] = [stop_time.arrival_time, stop_time.stop_id]
			self.departure[i] = [stop_time.departure_time, stop_time.stop_id]
			self.on_section[i-1] = [self.departure[i - 1], self.arrival[i]]

	def __init__(self, trip):
		self.trip = trip
		self.initialize_events()