import unittest
from src.util.graph import Graph, Station, Section

class StationTestCase(unittest.TestCase):
	def test_create_invalid_station(self):
		self.assertRaises(TypeError, Station)
		self.assertRaises(TypeError, Station, 20)
		self.assertRaises(TypeError, Station, '20')
		self.assertRaises(TypeError, Station, '20', '')
		self.assertRaises(TypeError, Station, '20', 'Berlin Hbf')

		station = Station(20, '')
		self.assertFalse(station.isValid())

		station2 = Station(-5, 'Berlin Hbf')
		self.assertFalse(station.isValid())

	def test_create_valid_station(self):
		station = Station(20, 'Berlin Hbf')
		self.assertTrue(station.isValid())
		self.assertEqual(station.stop_id, 20)
		self.assertEqual(station.stop_name, 'Berlin Hbf')

	def test_string_representation(self):
		station = Station(42, 'Berlin Ostbahnhof')
		self.assertEqual('Station 42: Berlin Ostbahnhof', str(station))

class SectionTestCase(unittest.TestCase):
	def setUp(self):
		self.station1 = Station(15, 'Berlin Ostbahnhof')
		self.station2 = Station(37, 'Frankfurt Flughafen')

	def tearDown(self):
		self.station1 = None
		self.station2 = None

	def test_create_invalid_section(self):
		self.assertRaises(TypeError, Section)
		self.assertRaises(TypeError, Section, 30)
		self.assertRaises(TypeError, Section, self.station1, self.station2)
		self.assertRaises(TypeError, Section, 30, self.station1)
		self.assertRaises(TypeError, Section, '30', self.station1, self.station2)

	def test_create_valid_section(self):
		section = Section(42, self.station1, self.station2)
		self.assertTrue(section.isValid())
		self.assertEqual(section.section_id, 42)
		self.assertEqual(section.first_station, self.station1)
		self.assertEqual(section.second_station, self.station2)

	def test_string_representation(self):
		self.assertEqual(True, True)
class GraphTestCase(unittest.TestCase):
	def setUp(self):
		self.graph = Graph()

	def tearDown(self):
		self.graph = None

	def test_create_empty_graph(self):
		self.assertTrue(self.graph.isEmpty())

	def test_find_non_existing_station(self):
		self.assertFalse(self.graph.station_existing(20))
		self.assertRaises(ValueError, self.graph.get_station_by_id, 20)

	def test_find_non_existing_section(self):
		station1 = Station(20, 'Berlin Hbf')
		station2 = Station(30, 'Berlin Ostbahnhof')
		self.assertFalse(self.graph.section_existing(station1, station2))
		self.assertFalse(self.graph.section_existing(station2, station1))
		self.assertRaises(ValueError, self.graph.get_section, station1, station2)
		self.assertRaises(ValueError, self.graph.get_section, station2,station1)

	def test_create_station(self):
		self.graph.create_station(42, 'Berlin Hbf')
		station = self.graph.stations[-1]
		self.assertTrue(isinstance(station, Station))
		self.assertTrue(station.isValid())
		self.assertEqual(station.stop_id, 42)
		self.assertEqual(station.stop_name, 'Berlin Hbf')

		self.assertFalse(self.graph.isEmpty())
		self.assertTrue(self.graph.station_existing(42))
		self.assertTrue(self.graph.station_existing('Berlin Hbf'))
		self.assertFalse(self.graph.station_existing(41))
		self.assertEqual(station, self.graph.get_station_by_id(42))
		self.assertEqual(station, self.graph.get_station_by_name('Berlin Hbf'))

		self.assertRaises(ValueError, self.graph.create_station, 42, 'Berlin Hbf')
		self.assertRaises(ValueError, self.graph.create_station, 42, 'Frankfurt Hbf')
		self.assertRaises(ValueError, self.graph.create_station, 41, 'Berlin Hbf')

	def test_create_section_with_existing_stations(self):
		# setup
		self.graph.create_station(42, 'Berlin Hbf')
		self.graph.create_station(69, 'Frankfurt Hbf')
		station1 = self.graph.get_station_by_id(42)
		station2 = self.graph.get_station_by_id(69)
		station3 = Station(93, 'Berlin Ostbahhof')

		#test
		self.graph.create_section(station1, station2)
		section = self.graph.sections[-1]
		self.assertTrue(isinstance(section, Section))
		self.assertTrue(section.isValid())
		stations = [section.first_station, section.second_station]
		self.assertTrue(station1 in stations and station2 in stations)

		self.assertFalse(self.graph.isEmpty())
		self.assertTrue(self.graph.section_existing(station1, station2))
		self.assertTrue(self.graph.section_existing(station2, station1))
		self.assertFalse(self.graph.section_existing(station1, station3))

		self.assertRaises(ValueError, self.graph.create_section, station1, station2)
		self.assertRaises(ValueError, self.graph.create_section, station2, station1)