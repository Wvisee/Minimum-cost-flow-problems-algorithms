# Python program for implementation of Ford Fulkerson algorithm
# This code is contributed by Neelam Yadav and William Visée
# https://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/
from ..graph_functions.api import *
from collections import defaultdict
from copy import copy, deepcopy
import sys

#Breath first search
def BFS(graph, src, dst, parent):
	# Mark all the vertices as not visited
	visited = [False]*(len(graph.nodes))
	# Create a queue for BFS
	queue = []
	# Mark the source node as visited and enqueue it
	s = src
	queue.append(s)
	visited[s] = True
	# Standard BFS Loop
	while queue:
		# Dequeue a vertex from queue and print it
		u = queue.pop(0)
		# Get all adjacent vertices of the dequeued vertex u
		# If a adjacent has not been visited, then mark it
		# visited and enqueue it
		for node in graph.neighbors(u):
			if not visited[node]:
				data = graph.get_edge_data(u, node)
				if data.get("flow")<data.get("capacity"):
					# If we find a connection to the sink node,
					# then there is no point in BFS anymore
					# We just have to set its parent and can return true
					if node == dst:
						visited[node] = True
						parent[node] = u
						return True
					queue.append(node)
					visited[node] = True
					parent[node] = u
	# We didn't reach sink in BFS starting
	# from source, so return false
	return False

# Returns tne maximum flow from s to t in the given graph
def FordFulkerson(graph, src, dst):
	# This array is filled by BFS and to store path
	parent = [-1]*(len(graph.nodes))
	max_flow = 0 # There is no flow initially
	# Augment the flow while there is path from source to sink
	while BFS(graph, src, dst, parent) :
		# Find minimum residual capacity of the edges along the
		# path filled by BFS. Or we can say find the maximum flow
		# through the path found.
		path_flow = float("Inf")
		s = dst
		while(s != src):
			#print(path_flow)
			data = graph.get_edge_data(parent[s],s)
			path_flow = min(path_flow, data.get("capacity")-data.get("flow"))
			s = parent[s]
		#TODO make condition to not pass max
		# Add path flow to overall flow
		max_flow += path_flow
		# update residual capacities of the edges and reverse edges
		# along the path
		v = dst
		while(v != src):
			u = parent[v]
			graph[u][v]["flow"] += path_flow
			#data["weight"] += path_flow
			v = parent[v]
	return graph,max_flow

def generic_augmenting_path(graph):
	source, sink = add_source_sink_maxflow(graph)
	graph, maxflow = FordFulkerson(graph, source, sink)
	#delete virtual edge that connect multiple source and sink
	remove_source_sink(graph, source, sink)
	return graph, maxflow
