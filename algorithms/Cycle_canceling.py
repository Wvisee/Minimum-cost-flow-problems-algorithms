from .max_flow_augmenting import *

def cycle_canceling(graph, src, dst):
    #Establish a feasible flow x in the network => max flow algorithms
    graph, max_flow = max_flow_augmenting_path(graph, src, dst)

    #transform graph to residual network
    residual_network = graph_to_residual(graph)

    #check negative path
    neg_cycle = NegCycleBellmanFord(residual_network, src, dst)
    print("negative circle is :", end=" ")
    print(neg_cycle)
    while len(neg_cycle)!=0:
        #augment units of Flow with min flow of the cycle in Gx
        residual_network = augment_graph(residual_network,neg_cycle)

        #find next negative cycle
        neg_cycle = NegCycleBellmanFord(residual_network, src, dst)
        print("negative circle is :", end=" ")
        print(neg_cycle)
    #residual network back to graph
    graph = residual_to_graph(residual_network)
    #print solution
    print(max_flow)
    print_graph(graph)

# The main function that finds shortest distances
# from src to all other vertices using Bellman-
# Ford algorithm.  The function also detects
# negative weight cycle
#https://www.geeksforgeeks.org/detect-negative-cycle-graph-bellman-ford/
#https://www.geeksforgeeks.org/print-negative-weight-cycle-in-a-directed-graph/
# Function runs Bellman-Ford algorithm
# and prints negative cycle(if present)
def NegCycleBellmanFord(graph, src, dst):
    V = len(graph.nodes)
    E = len(graph.edges)
    dist =[float("Inf") for i in range(V)]
    parent =[-1 for i in range(V)]
    dist[src] = 0;

    # Relax all edges |V| - 1 times.
    for i in range(1, V):
        for u,v in graph.edges:

            weight = graph[u][v]["weight"]

            if (dist[u] != float("Inf") and
                dist[u] + weight < dist[v]):

                dist[v] = dist[u] + weight;
                parent[v] = u;

    # Check for negative-weight cycles
    C = -1;
    for u,v in graph.edges:

        weight = graph[u][v]["weight"]

        if (dist[u] != float("Inf") and
            dist[u] + weight < dist[v]):

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
