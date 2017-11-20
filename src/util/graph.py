# Graph class
# Use getOrCreateVertex(stop_id, stop_name) for vertices
# Use getOrCreateEdge(start_stop_id, end_stop_id) for edges

class Graph:
	def __init__(self):
		self.edges = []
		self.vertices = []
		self.highest_id = 0

	def getOrCreateVertex(stop_id, stop_name):
		vertex = self.vertex(stop_id)
		if not vertex.isValid():
			vertex = _Vertex(stop_id, stop_name)
			if not vertex.isValid():
				return vertex
			self.vertices.append(vertex)
		return vertex

	def getOrCreateEdge(start_stop_id, end_stop_id):
		start_vertex = self.getOrCreateVertex(start_stop_id)
		end_vertex = self.getOrCreateVertex(end_stop_id)
		if not (start_vertex.isValid() and end_vertex.isValid()):
			return _Vertex()
		return self._getOrCreateEdge(start_vertex, end_vertex)

	def _getOrCreateEdge(first_vertex, second_vertex):
		edge = self.edge(first_vertex, second_vertex)
		if not edge.isValid():
			edge = _Edge(self.highest_id, first_vertex, second_vertex)
			highest_id += 1
			first_vertex.addIncident(second_vertex, edge)
			second_vertex.addIncident(first_vertex, edge)
			self.edges.append(edge)
		return edge

	def _vertex(stop_id):
		for v in vertices:
			if (v.stop_id == stop_id):
				return v
		return Vertex()

	def _edge(first_vertex, second_vertex):
		for e in edges:
			if (e.first_vertex == start_stop_id and e.second_vertex == end_stop_id or
				e.second_vertex == start_stop_id and e.first_vertex == end_stop_id):
				return e
		return Edge()

# private Vertex class for Graph, only instantiate over Graph class
class _Vertex:
	def __init__(self, stop_id, stop_name):
		self.stop_id = stop_id
		self.stop_name = stop_name
		self.incidents = []

	def isValid():
		return False if (self.stop_id is None) else True

	def addIncident(vertex, edge):
		self.incidents.append([vertex, edge])

# private Edge class for Graph, only instantiate over Graph class
class _Edge:
	def __init__(self, first_vertex, second_vertex):
		self.first_vertex = first_vertex
		self.second_vertex = second_vertex

	def isValid():
		return False if (self.first_stop_id is None or self.second_stop_id is None) else True