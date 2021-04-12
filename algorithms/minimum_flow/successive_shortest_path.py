import networkx as nx
import sys

def successive_shortest_path(graph):
    x = 0
    e = [0 for i in range(len(graph.nodes()))]
    pi = [0 for i in range(len(graph.nodes()))]
    s = [] #node number being source
    t = [] #node number being sink

    for node in graph.nodes():
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            e[node] = i
            if i < 0:
                t.append(node)
            elif i > 0:
                s.append(node)
    #debugging
    #print(e)
    #print(s)
    #print(t)

    residual = graph_to_residual(graph)

    while len(s)!=0:
        source = s.pop()
        sink = t.pop()

        print(x)
        print(pi)
        print(e)
        print_graph(residual)

        #update pi
        for node in residual.nodes():
            small_path = nx.shortest_path(residual, source=source, target=node, weight="weight")
            weight = 0
            for i in range(len(small_path)-1):
                node_a = small_path[i]
                node_b = small_path[i+1]
                weight += residual[node_a][node_b]["weight"]
            pi[node] = pi[node] -weight
        #find smallest path
        smallest_path = nx.shortest_path(residual, source=source, target=sink, weight="weight")
        #update residual_cost
        for u,v in residual.edges():
            if residual[u][v]["weight"]!=0:
                residual[u][v]["weight"] = residual[u][v]["weight"] - pi[u] + pi[v]
                if residual[u][v]["weight"] < 0:
                    residual[u][v]["weight"] = 0
        #find min e(source), e(sink), {rij e Path}
        min_aug = sys.maxsize
        for i in range(len(smallest_path)-1):
            node_a = smallest_path[i]
            node_b = smallest_path[i+1]
            min_aug = min(min_aug,residual[node_a][node_b]["residual"])
        min_aug = min(min_aug, e[source], - e[sink])
        #update x
        x = x + min_aug
        #update residual_graph
        add_flow_to_residual(residual, smallest_path, min_aug)
        #update E and D
        e[source] -= min_aug
        if e[source]>0:
            s.append(source)
        e[sink] += min_aug
        if e[sink]<0:
            t.append(sink)

        print(x)
        print(pi)
        print(e)
        print(smallest_path)
        print_graph(residual)

    #solution
    print(x)
    #print_graph(residual_to_graph(residual,graph)) #initial graph is necessairy to find weight has in process all cost are nearly 0
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

def residual_to_graph(residual_network, initial_graph):
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
