import unittest
from src.util.graph import Graph, Station, Section

class StationTestCase(unittest.TestCase):
	def test_create_invalid_station(self):
		self.assertRaises(TypeError, Station)
		self.assertRaises(TypeError, Station, 20)
		self.assertRaises(TypeError, Station, "20")
		self.assertRaises(TypeError, Station, "20", "")
		self.assertRaises(TypeError, Station, "20", "Berlin Hbf")

		station = Station(20, "")
		self.assertFalse(station.isValid())

		station2 = Station(-5, "Berlin Hbf")
		self.assertFalse(station.isValid())

	def test_create_valid_station(self):
		station = Station(20, "Berlin Hbf")
		self.assertTrue(station.isValid())
		self.assertEqual(station.stop_id, 20)
		self.assertEqual(station.stop_name, "Berlin Hbf")	

class SectionTestCase(unittest.TestCase):
	def setUp(self):
		self.station1 = Station(15, "Berlin Ostbahnhof")
		self.station2 = Station(37, "Frankfurt Flughafen")

	def tearDown(self):
		self.station1 = None
		self.station2 = None

	def test_create_invalid_section(self):
		self.assertRaises(TypeError, Section)
		self.assertRaises(TypeError, Section, 30)

	def test_create_valid_section(self):
		section = Section(42, self.station1, self.station2)
		self.assertTrue(section.isValid())
		self.assertEqual(section.stop_id, 42)
		self.assertEqual(section.first_station, self.station1)
		self.assertEqual(section.second_station, self.station2)

class GraphTestCase(unittest.TestCase):
	def test_create_empty_graph(self):
		graph = Graph()
		self.assertTrue(graph.isEmpty())