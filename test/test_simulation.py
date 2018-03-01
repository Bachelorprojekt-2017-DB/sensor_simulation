import unittest
import datetime
from src import Simulation

class SimulationTestCase(unittest.TestCase):
	def test_simulation_creation(self):
		simulation = Simulation()
		self.assertEqual(simulation.earliest_time, datetime.timedelta.max)
		self.assertEqual(simulation.latest_time, datetime.timedelta.min)

	def test_simulation_timestep_calculation(self):
		simulation = Simulation()
		self.assertEqual(simulation.timedelta_to_minutes(datetime.timedelta(minutes = 42)), 42)
