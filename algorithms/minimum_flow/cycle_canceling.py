from ..maximum_flow.preflow_push import *
from ..graph_functions.api import *

'''
Cycle Canceling
1   Establish a feasible flow x in the network
2   While G_x contains a negative cycle
3       identify a negative cycle W
4       sigma = min(r_i_j : (i,j) in W)
5       augment sigma units of flow along the cycle W
6       update G_x
'''

def cycle_canceling(graph):
    #link all source together with a source node, link all sink together with a sink node
    source, sink = add_source_sink_mincost(graph)
    #Establish a feasible flow x in the network => max flow algorithms
    graph, max_flow = preflow_push(graph)
    #transform graph to residual network
    residual_network = graph_to_residual(graph)
    #check negative path
    neg_cycle = NegCycleBellmanFord(residual_network, source, sink)
    #print("negative circle is :", end=" ")
    while len(neg_cycle)!=0:
        #augment units of Flow with min flow of the cycle in Gx
        residual_network = augment_graph(residual_network,neg_cycle)
        #find next negative cycle
        neg_cycle = NegCycleBellmanFord(residual_network, source, sink)
        #print("negative circle is :", end=" ")
        #print(neg_cycle)
    #find optimal flow
    flow = 0
    for node in residual_network.neighbors(sink):
        flow += residual_network[sink][node]["residual"]
    #residual network back to graph
    graph = residual_to_graph(residual_network)
    #delete virtual edge that connect multiple source and sink
    remove_source_sink(graph, source, sink)
    #compute total cost of flow
    total_cost = compute_total_cost(graph)
    #print solution
    return graph, flow, total_cost

#The function detects negative weight cycle
#adapted from the following website
#https://www.geeksforgeeks.org/print-negative-weight-cycle-in-a-directed-graph/
def NegCycleBellmanFord(graph, src, dst):
    V = len(graph.nodes)
    E = len(graph.edges)
    dist =[sys.maxsize for i in range(V)]
    parent =[-1 for i in range(V)]
    dist[src] = 0;
    # Relax all edges |V| - 1 times.
    for i in range(1, V):
        for u,v in graph.edges:
            weight = graph[u][v]["weight"]
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight;
                parent[v] = u;
    # Check for negative-weight cycles
    C = -1;
    for u,v in graph.edges:
        weight = graph[u][v]["weight"]
        if dist[u] + weight < dist[v]:
            # Store one of the vertex of
            # the negative weight cycle
            C = v;
            break;

    if (C != -1):
        for i in range(V):
            C = parent[C];
        # To store the cycle vertex
        cycle = []
        v = C
        while (True):
            cycle.append(v)
            if (v == C and len(cycle) > 1):
                break;
            v = parent[v]
        # Reverse cycle[]
        cycle.reverse()
        # Printing the negative cycle
        return cycle
    else:
        return []

#augment a negative cycle toward the moment when it isn't a negative cycle
def augment_graph(graph,neg_cycle):
    list_to_del = []
    list_to_add = []
    graph = graph.copy()

    min_flow = float("Inf")
    for i in range(len(neg_cycle)-1):
        node_a = neg_cycle[i]
        node_b = neg_cycle[i+1]
        min_flow = min(min_flow,graph[node_a][node_b]["residual"])

    for i in range(len(neg_cycle)-1):
        u = neg_cycle[i]
        v = neg_cycle[i+1]
        residual = graph[u][v]["residual"]
        weight = graph[u][v]["weight"]
        if residual==min_flow:
            list_to_del.append((u,v))
            if graph.has_edge(v,u):
                graph[v][u]["residual"]+= min_flow
            else:
                list_to_add.append((v,u,-weight,min_flow))
        else:
            graph[u][v]["residual"]-= min_flow
            if graph.has_edge(v,u):
                graph[v][u]["residual"]+= min_flow
            else:
                list_to_add.append((v,u,-weight,min_flow))

    for u,v in list_to_del:
        graph.remove_edge(u,v)
    for u,v,w,c in list_to_add:
        graph.add_edge(u, v, weight=w, residual=c)
    return graph
