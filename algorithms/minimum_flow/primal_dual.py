import networkx as nx
from ..maximum_flow.generic_augmenting_path import *

'''
Primal-Dual
1    Transform network G by adding source and sink
2    Initial flow x is zero
3    Use Bellman-Ford’s algorithm to establish potentials pi
4    Reduce Cost (pi)
5    while ( Gx contains a path from s to t ) do
6        Calculate node potential  using Dijkstra’s algorithm
7        Reduce Cost (pi)
8        Establish a maximum flow y from s to t in
9        x  <- x + y
'''

def primal_dual(graph):
    #var flow
    flow = 0
    #find sinks and sources
    s_bag = []
    t_bag = []
    for node in graph.nodes():
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            if i < 0:
                t_bag.append((node,-i))
            elif i > 0:
                s_bag.append((node,i))
    #add a new source node that attach all sources
    source = len(graph.nodes()) #new node id
    for node,i in s_bag:
        graph.add_edge(source, node, weight=0, capacity=i, flow=0)
    #add a new sink node that attach all sinks
    sink = len(graph.nodes()) #new node id
    for node,i in t_bag:
        graph.add_edge(node, sink, weight=0, capacity=i, flow=0)
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
    #reduce cost
    for u,v in graph.edges():
        graph[u][v]["weight"] = graph[u][v]["weight"] + pi[u] - pi[v]
        if graph.has_edge(v,u):
            graph[u][v]["weight"] = 0
    #transform graph to residual graph
    residual = graph_to_residual(graph)
    #find if path exist between s and t
    if nx.has_path(residual, source=source, target=sink):
        path = nx.bellman_ford_path(residual, source=source, target=sink, weight="weight")
    else:
        path=[]

    while len(path)!=0:
        #update potentials
        pi = [0 for i in range(len(residual.nodes()))]
        for node in graph.nodes():
            small_path = nx.shortest_path(residual, source=source, target=node, weight="weight")
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
        #find admissible residual network
        admissible = residual.copy()
        list_to_del = []
        for u,v in admissible.edges():
            if admissible[u][v]["weight"]!=0:
                list_to_del.append((u,v))
        for u,v in list_to_del:
            admissible.remove_edge(u,v)
        #find max flow in admissible residual network
        admissible = residual_to_graph(admissible)
        graph, maxflow = generic_augmenting_path(admissible,source,sink)
        #update residual
        for u,v in admissible.edges():
            edge_flow = admissible[u][v]["flow"]
            if edge_flow > 0:
                add_flow_to_residual(residual,[u,v],edge_flow)
        #update counter flow
        flow = flow + maxflow
        #find if path exist between s and t
        if nx.has_path(residual, source=source, target=sink):
            path = nx.bellman_ford_path(residual, source=source, target=sink, weight="weight")
        else:
            path=[]
    print(flow)
    print_graph(residual)

def add_flow_to_residual(graph, path, flow):
    list_to_del = []
    list_to_add = []
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        residual = graph[u][v]["residual"]
        weight = graph[u][v]["weight"]
        if graph.has_edge(v,u):
            if residual==flow:
                list_to_del.append((u,v))
                list_to_del.append((v,u))
                residual_inv = graph[v][u]["residual"]
                weight_inv = graph[v][u]["weight"]
                list_to_add.append((v,u, weight_inv, residual_inv+flow))
            elif residual>flow:
                list_to_del.append((u,v))
                list_to_del.append((v,u))
                residual_inv = graph[v][u]["residual"]
                weight_inv = graph[v][u]["weight"]
                list_to_add.append((u,v, weight, residual-flow))
                list_to_add.append((v,u, weight_inv, residual_inv+flow))
        else:
            if residual==flow:
                list_to_del.append((u,v))
                list_to_add.append((v,u, -weight, residual))
            elif residual>flow:
                list_to_del.append((u,v))
                list_to_add.append((u,v,weight,residual-flow))
                list_to_add.append((v,u,-weight,flow))
    for u,v in list_to_del:
        graph.remove_edge(u,v)
    for u,v,w,c in list_to_add:
        graph.add_edge(u, v, weight=w, residual=c)

def graph_to_residual(graph):
    list_to_del = []
    list_to_add = []
    residual = graph.copy()
    for u,v in residual.edges():
        flow = residual[u][v]["flow"]
        capacity = residual[u][v]["capacity"]
        weight = residual[u][v]["weight"]
        if flow==capacity:
            #create opposite edge with negative weight
            list_to_add.append((v,u,-weight,capacity))
            #update the current edge
            list_to_del.append((u,v))
        elif 0<flow<capacity:
            #create opposite edge with negative weight
            list_to_add.append((v,u,-weight,flow))
            #update the current edge
            list_to_add.append((u,v,weight,capacity-flow))
            list_to_del.append((u,v))
        elif flow==0:
            list_to_add.append((u,v,weight,capacity))
            list_to_del.append((u,v))
    for u,v in list_to_del:
        residual.remove_edge(u,v)
    for u,v,w,c in list_to_add:
        residual.add_edge(u, v, weight=w, residual=c)
    return residual

#not really converting into a graph but it is sufficent to compute the maxflow of the admissible residual
def residual_to_graph(residual_network):
    list_to_del = []
    list_to_add = []
    graph = residual_network.copy()
    for u,v in graph.edges():
        residual = graph[u][v]["residual"]
        weight = graph[u][v]["weight"]
        list_to_del.append((u,v))
        list_to_add.append((u,v,residual,weight))
    for u,v in list_to_del:
        graph.remove_edge(u,v)
    for u,v,w,c in list_to_add:
        graph.add_edge(u, v, capacity=w, flow=c)
    return graph


def print_graph(graph):
    for a,b in graph.edges():
        print(str(a)+","+str(b)+" = "+str(graph.get_edge_data(a,b)))
