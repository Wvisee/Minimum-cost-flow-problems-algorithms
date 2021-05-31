import networkx as nx
from ..maximum_flow.generic_augmenting_path import *
from ..graph_functions.api import *

'''
Primal-Dual
1   x: = 0 and pi : = 0;
2   e(s) : = b(s) and e(t) : = b(t);
3   while e(s) > 0 do
4       determine shortest path distances d(·) from node s to all other nodes in G(x) with
        respect to the reduced costs c_pi_ij;
6       update pi : = pi - d;
7       define the admissible network GO(x);
8       establish a maximum flow from node s to node t in GO(x);
9       update e(s) , e(t), and G(x);
'''

def primal_dual(graph):
    #var flow
    flow = 0
    #add source and sink
    source, sink = add_source_sink_mincost(graph)
    #find potentials
    pi = [0 for i in range(len(graph.nodes()))]
    # init node excess
    e = graph.nodes[source]['b']
    #transform graph to residual graph
    residual = graph_to_residual_primal(graph)
    #copy a graph that we will use to return the solution as the current graph will have modified weight
    residual_return = graph_to_residual(graph.copy())
    while e>0:
        #update potentials
        pi = [0 for i in range(len(residual.nodes()))]
        for node in residual.nodes():
            small_path = nx.shortest_path(residual, source=source, target=node, weight="weight")
            weight = 0
            for i in range(len(small_path)-1):
                node_a = small_path[i]
                node_b = small_path[i+1]
                weight += residual[node_a][node_b]["weight"]
            pi[node] = weight
        #reduce cost
        for u,v in residual.edges():
            residual[u][v]["weight"] = residual[u][v]["weight"] + pi[u] - pi[v]
            if residual.has_edge(v,u):
                residual[u][v]["weight"] = 0
        #find admissible residual network
        admissible = residual.copy()
        list_to_del = []
        for u,v in admissible.edges():
            w = admissible[u][v]["weight"]
            if w!=0:
                list_to_del.append((u,v))
        for u,v in list_to_del:
            admissible.remove_edge(u,v)
        #find max flow in admissible residual network
        admissible = residual_to_graph_primal(admissible)
        admissible, admissible_maxflow = generic_augmenting_path(admissible)
        #add flow to residual
        for u,v in admissible.edges():
            maxflow = admissible[u][v]["flow"]
            if maxflow > 0:
                if residual.has_edge(u,v): #else already at maximum capacity
                    max_to_add = residual[u][v]["residual"]
                    if residual.has_edge(v,u):#some flow
                        if residual[v][u]["residual"]==maxflow:#means no more flow to add
                            continue
                        else:
                            flow_to_add = maxflow - residual[v][u]["residual"]
                    else:#situation where no flow
                        flow_to_add = maxflow
                    add_flow_to_residual_primal(residual,[u,v],flow_to_add)
                    add_flow_to_residual(residual_return,[u,v],flow_to_add)
        #update e
        e = e - admissible_maxflow
        #update total flow
        flow = flow + admissible_maxflow

    #delete virtual edge that connect multiple source and sink
    remove_source_sink(residual_return, source, sink)
    #residual network back to graph
    graph = residual_to_graph(residual_return)
    #compute total cost of flow
    total_cost = compute_total_cost(graph)
    #return solution
    return graph, flow, total_cost

#add flow to a residual graph
#we don't use the api function because the weight in this graph can be 0
#so a new functions for this purpose has been developped
def add_flow_to_residual_primal(graph, path, flow):
    list_to_del = []
    list_to_add = []
    for i in range(len(path)-1):
        u = path[i]
        v = path[i+1]
        residual = graph[u][v]["residual"]
        weight = graph[u][v]["weight"]
        ini_way = graph[u][v]["ini_way"]
        if graph.has_edge(v,u):
            if residual==flow:
                list_to_del.append((u,v))
                list_to_del.append((v,u))
                residual_inv = graph[v][u]["residual"]
                weight_inv = graph[v][u]["weight"]
                list_to_add.append((v,u, weight_inv, residual_inv+flow, not ini_way))
            elif residual>flow:
                list_to_del.append((u,v))
                list_to_del.append((v,u))
                residual_inv = graph[v][u]["residual"]
                weight_inv = graph[v][u]["weight"]
                list_to_add.append((u,v, weight, residual-flow, ini_way))
                list_to_add.append((v,u, weight_inv, residual_inv+flow, not ini_way))
        else:
            if residual==flow:
                list_to_del.append((u,v))
                list_to_add.append((v,u, -weight, residual, not ini_way))
            elif residual>flow:
                list_to_del.append((u,v))
                list_to_add.append((u,v,weight,residual-flow, ini_way))
                list_to_add.append((v,u,-weight,flow, not ini_way))
    for u,v in list_to_del:
        graph.remove_edge(u,v)
    for u,v,w,c,i in list_to_add:
        graph.add_edge(u, v, weight=w, residual=c, ini_way=i)

#transform a graph to a residual graph
#we don't use the api function because the weight in this graph can be 0
#so a new functions for this purpose has been developped
def graph_to_residual_primal(graph):
    list_to_del = []
    list_to_add = []
    residual = graph.copy()
    for u,v in residual.edges():
        flow = residual[u][v]["flow"]
        capacity = residual[u][v]["capacity"]
        weight = residual[u][v]["weight"]
        if flow==capacity:
            #create opposite edge with negative weight
            list_to_add.append((v,u,-weight,capacity, False))
            #update the current edge
            list_to_del.append((u,v))
        elif 0<flow<capacity:
            #create opposite edge with negative weight
            list_to_add.append((v,u,-weight,flow, False))
            #update the current edge
            list_to_add.append((u,v,weight,capacity-flow, True))
            list_to_del.append((u,v))
        elif flow==0:
            list_to_add.append((u,v,weight,capacity, True))
            list_to_del.append((u,v))
    for u,v in list_to_del:
        residual.remove_edge(u,v)
    for u,v,w,c,i in list_to_add:
        residual.add_edge(u, v, weight=w, residual=c, ini_way=i)
    return residual

#transform a residual graph to a graph
#we don't use the api function because the weight in this graph can be 0
#so a new functions for this purpose has been developped
def residual_to_graph_primal(residual_network):
    list_to_del = []
    list_to_add = []
    graph = residual_network.copy()
    for u,v in graph.edges():
        residual = graph[u][v]["residual"]
        weight = graph[u][v]["weight"]
        ini_way = graph[u][v]["ini_way"]
        if graph.has_edge(v,u):
            if ini_way:
                opo_residual = graph[v][u]["residual"]
                capacity = residual + opo_residual
                list_to_del.append((u,v))
                list_to_del.append((v,u))
                list_to_add.append((u,v,weight,capacity,opo_residual))
        else:
            if ini_way:
                list_to_del.append((u,v))
                list_to_add.append((u,v,weight,residual,0))
            else:
                list_to_del.append((u,v))
                list_to_add.append((v,u,weight,residual,residual))

    for u,v in list_to_del:
        graph.remove_edge(u,v)
    for u,v,w,c,f in list_to_add:
        graph.add_edge(u, v, weight=w, capacity=c, flow=f)
    return graph
