import networkx as nx
import sys
from ..graph_functions.api import *

'''
Successive Shortest Path with potentials
1    Transform network G by adding source and sink
2    Initial flow x is zero
3    Use Bellman-Ford’s algorithm to establish potentials pi
4    Reduce Cost (pi)
5    while ( Gx contains a path from s to t ) do
6        Find any shortest path P from s to t
7        Reduce Cost (pi)
8        Augment current flow x along P
9        update Gx
'''

def successive_shortest_path(graph):
    source, sink = add_source_sink_mincost(graph)
    #var flow
    flow = 0
    #find potentials
    pi = [0 for i in range(len(graph.nodes()))]
    for node in graph.nodes():
        small_path = nx.bellman_ford_path(graph, source=source, target=node, weight="weight")
        weight = 0
        for i in range(len(small_path)-1):
            node_a = small_path[i]
            node_b = small_path[i+1]
            weight += graph[node_a][node_b]["weight"]
        pi[node] = pi[node] + weight
    #copy a graph that we will use to return the solution as the current graph will have modified weight
    residual_return = graph_to_residual(graph.copy())
    #reduce cost
    for u,v in graph.edges():
        graph[u][v]["weight"] = graph[u][v]["weight"] + pi[u] - pi[v]
        if graph.has_edge(v,u):
            graph[u][v]["weight"] = 0
    #to_residual
    residual = graph_to_residual(graph)
    if nx.has_path(residual, source=source, target=sink):
        path = nx.bellman_ford_path(residual, source=source, target=sink, weight="weight")
    else:
        path=[]

    while len(path)!=0:
        #update potentials
        pi = [0 for i in range(len(residual.nodes()))]
        for node in graph.nodes():
            small_path = nx.bellman_ford_path(residual, source=source, target=node, weight="weight")
            weight = 0
            for i in range(len(small_path)-1):
                node_a = small_path[i]
                node_b = small_path[i+1]
                weight += residual[node_a][node_b]["weight"]
            pi[node] = pi[node] + weight
        #reduce cost
        for u,v in residual.edges():
            residual[u][v]["weight"] = residual[u][v]["weight"] + pi[u] - pi[v]
            if residual.has_edge(v,u):
                residual[u][v]["weight"] = 0
        #find best flow
        min_aug = sys.maxsize
        for i in range(len(path)-1):
            node_a = path[i]
            node_b = path[i+1]
            min_aug = min(min_aug,residual[node_a][node_b]["residual"])
        #augment flow along P
        flow = flow + min_aug
        #update Gx
        add_flow_to_residual(residual, path, min_aug)
        add_flow_to_residual(residual_return, path, min_aug)
        #find if path exist
        if nx.has_path(residual, source=source, target=sink):
            path = nx.bellman_ford_path(residual, source=source, target=sink, weight="weight")
        else:
            path=[]

    #delete virtual edge that connect multiple source and sink
    remove_source_sink(residual_return, source, sink)
    #residual network back to graph
    graph = residual_to_graph(residual_return)
    #compute total cost of flow
    total_cost = compute_total_cost(graph)
    #return solution
    return graph, flow, total_cost
