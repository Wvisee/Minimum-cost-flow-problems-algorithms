import networkx as nx
import sys

#add flow to the residual graph
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

#transform a graph to a residual graph
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

#transform a residual graph to a graph
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
            elif weight==0:
                opo_residual = graph[v][u]["residual"]
                if graph.nodes[u]['b']>0: #if u == source
                    capacity = opo_residual + residual
                    list_to_del.append((u,v))
                    list_to_del.append((v,u))
                    list_to_add.append((u,v,weight,capacity, opo_residual))
                elif graph.nodes[v]['b']<0: #if v ==sink
                    capacity = opo_residual + residual
                    list_to_del.append((u,v))
                    list_to_del.append((v,u))
                    list_to_add.append((u,v,weight,capacity, opo_residual))
        else:
            if weight<0:
                list_to_del.append((u,v))
                list_to_add.append((v,u,-weight,residual, residual))
            elif weight>0:
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

#compute the total cost of a flow through a graph
def compute_total_cost(graph):
    total_cost = 0
    for a,b in graph.edges():
        x = graph[a][b]["flow"]
        if x > 0:
            total_cost += x * graph[a][b]["weight"]
    return total_cost

#attach all the source node to one single node
#attach all the sink node to one single node
#the capacity of the edges will be infinite
def add_source_sink_maxflow(graph):
    #find sinks and sources
    s_bag = []
    t_bag = []
    for node in graph.nodes():
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            if i < 0:
                t_bag.append(node)
                del graph.nodes[node]['b']
                graph.nodes[node]['c'] = i
            elif i > 0:
                s_bag.append(node)
                del graph.nodes[node]['b']
                graph.nodes[node]['c'] = i
    #add a new source node that attach all sources
    source = len(graph.nodes()) #new node id
    for node in s_bag:
        graph.add_edge(source, node, weight=0, capacity=sys.maxsize, flow=0)
    graph.nodes[source]['b'] = 1
    #add a new sink node that attach all sinks
    sink = len(graph.nodes()) #new node id
    for node in t_bag:
        graph.add_edge(node, sink, weight=0, capacity=sys.maxsize, flow=0)
    graph.nodes[sink]['b'] = -1
    return source, sink

def add_source_sink_maxflow_rsp_with_constraint(graph):
    #find sinks and sources
    s_bag = []
    t_bag = []
    for node in graph.nodes():
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            if i < 0:
                t_bag.append(node)
                del graph.nodes[node]['b']
                graph.nodes[node]['c'] = i
            elif i > 0:
                s_bag.append(node)
                del graph.nodes[node]['b']
                graph.nodes[node]['c'] = i
    #add a new source node that attach all sources
    source = len(graph.nodes()) #new node id
    for node in s_bag:
        #get max flow that can go out the node and put it has the capacity of source -> node
        total = 0
        for i,j in graph.edges():
            if i==node:
                total = total + graph[i][j]["capacity"]
        graph.add_edge(source, node, weight=0, capacity=total, flow=0)
    graph.nodes[source]['b'] = 1
    #add a new sink node that attach all sinks
    sink = len(graph.nodes()) #new node id
    for node in t_bag:
        #get max flow that can go out the node and put it has the capacity of source -> node
        total = 0
        for i,j in graph.edges():
            if j==node:
                total = total + graph[i][j]["capacity"]
        graph.add_edge(node, sink, weight=0, capacity=total, flow=0)
    graph.nodes[sink]['b'] = -1
    return source, sink

#attach all the source node to one single node
#attach all the sink node to one single node
#the capacity of the edges will be egal to the demand/offer of the node
def add_source_sink_mincost(graph):
    #find sinks and sources
    s_bag = []
    t_bag = []
    for node in graph.nodes():
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            if i < 0:
                t_bag.append((node,i))
                del graph.nodes[node]['b']
                graph.nodes[node]['c'] = i
            elif i > 0:
                s_bag.append((node,i))
                del graph.nodes[node]['b']
                graph.nodes[node]['c'] = i
    #add a new source node that attach all sources
    source = len(graph.nodes()) #new node id
    sum_of_offer = 0
    for node,i in s_bag:
        graph.add_edge(source, node, weight=0, capacity=i, flow=0)
        sum_of_offer += i
    graph.nodes[source]['b'] = sum_of_offer
    #add a new sink node that attach all sinks
    sum_of_demand = 0
    sink = len(graph.nodes()) #new node id
    for node,i in t_bag:
        graph.add_edge(node, sink, weight=0, capacity=-i, flow=0)
        sum_of_demand += i
    graph.nodes[sink]['b'] = sum_of_demand
    return source, sink

#delete the node that link the sources
#delete the node that link the sinks
def remove_source_sink(graph, source, sink):
    s_bag = []
    t_bag = []
    for node in graph.nodes():
        if 'c' in graph.nodes[node] and (node in graph.neighbors(source) or node in graph.neighbors(sink)):
            graph.nodes[node]['b'] = graph.nodes[node]['c']
            del graph.nodes[node]['c']
    graph.remove_node(source)
    graph.remove_node(sink)

def get_source_sink(graph):
    source = 0
    sink = 0
    for node in graph.nodes():
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            if i < 0:
                sink = node
            elif i > 0:
                source = node
    return source, sink

#print all the edges and the data contained in the edges
def print_graph(graph):
    for a,b in graph.edges():
        print(str(a)+","+str(b)+" = "+str(graph.get_edge_data(a,b)))

def print_matrix(A):
    for i in range(len(A)):
        for j in range(len(A[0])):
            print(str(A[i,j])+" ", end='')
        print("")
