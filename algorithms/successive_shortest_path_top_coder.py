import networkx as nx
import sys

'''
Successive Shortest Path with potentials
1    Transform network G by adding source and sink
2    Initial flow x is zero
3    Use Bellman-Ford’s algorithm to establish potentials
4    Reduce Cost (  )
5    while ( Gx contains a path from s to t ) do
6        Find any shortest path P from s to t
7        Reduce Cost (  )
8        Augment current flow x along P
9        update Gx
'''

def successive_shortest_path(graph):
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

    #print_graph(graph)

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
    #print(pi)
    #reduce cost
    for u,v in graph.edges():
        graph[u][v]["weight"] = graph[u][v]["weight"] + pi[u] - pi[v]
        if graph.has_edge(v,u):
            graph[u][v]["weight"] = 0
    #print_graph(graph)
    #to_residual
    residual = graph_to_residual(graph)
    if nx.has_path(residual, source=source, target=sink):
        path = nx.bellman_ford_path(residual, source=source, target=sink, weight="weight")
    else:
        path=[]

    while len(path)!=0:
        pi = [0 for i in range(len(residual.nodes()))]
        for node in graph.nodes():
            small_path = nx.bellman_ford_path(residual, source=source, target=node, weight="weight")
            weight = 0
            for i in range(len(small_path)-1):
                node_a = small_path[i]
                node_b = small_path[i+1]
                weight += residual[node_a][node_b]["weight"]
            pi[node] = pi[node] + weight
        #print(pi)
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
        #print_graph(residual)
        #find if path exist
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
                list_to_add.append((v,u,weight,flow))
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

def residual_to_graph(residual_network):
    list_to_del = []
    list_to_add = []
    graph = residual_network.copy()
    for u,v in graph.edges():
        residual = graph[u][v]["residual"]
        weight = graph[u][v]["weight"]
        if graph.has_edge(v,u):
            if weight<0:
                capacity = graph[u][v]["residual"] + graph[v][u]["residual"]
                list_to_add.append((v,u,-weight,capacity, residual))
                list_to_del.append((u,v))
                list_to_del.append((v,u))
        else:
            if weight<0:
                list_to_del.append((u,v))
                list_to_add.append((v,u,-weight,residual, residual))
            else:
                list_to_del.append((u,v))
                list_to_add.append((u,v,weight,residual,0))

    for u,v in list_to_del:
        graph.remove_edge(u,v)
    for u,v,w,c,f in list_to_add:
        graph.add_edge(u, v, weight=w, capacity=c, flow=f)
    return graph


def print_graph(graph):
    for a,b in graph.edges():
        print(str(a)+","+str(b)+" = "+str(graph.get_edge_data(a,b)))
