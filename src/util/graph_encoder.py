import json
from .graph import Graph

class GraphEncoder():
	def create_station_dictionary(self, stations):
		station_dict = {}
		for station in stations:
			station_dict[station.stop_id] = station.stop_name
		return station_dict

	def create_section_dictionary(self, sections):
		section_dict = {}
		for section in sections:
			section_dict[section.section_id] = [section.first_station.stop_id, section.second_station.stop_id]
		return section_dict

	def create_graph_dictionary(self, graph):
		station_dict = self.create_station_dictionary(graph.stations.values())
		section_dict = self.create_section_dictionary(graph.sections)
		return {'stations': station_dict, 'sections': section_dict}

	def save_to_file(self, graph, path):
		json_dict = self.create_graph_dictionary(graph)
		with open(path, 'w') as file:
			file.write(json.dumps(json_dict, indent=4))

class GraphDecoder():
	def create_stations(self, graph, stations_dict):
		for key in stations_dict:
			graph.create_station(int(key), stations_dict[key])

	def create_sections(self, graph, sections_dict):
		for key in sections_dict:
			value = sections_dict[key]
			first_station = graph.get_station_by_id(int(value[0]))
			second_station = graph.get_station_by_id(int(value[1]))
			graph.create_section(first_station, second_station)

	def load_from_file(self, path):
		with open(path, 'r') as file:
			json_string = file.read()
		json_object = json.loads(json_string)
		graph = Graph()
		self.create_stations(graph, json_object['stations'])
		self.create_sections(graph, json_object['sections'])
		return graph
