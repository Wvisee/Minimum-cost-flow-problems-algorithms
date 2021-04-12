import networkx as nx

def preflow_push(graph):
    # add one source and one sink that connect multiple source and sink
    source, sink = add_source_sink(graph)
    #transform graph to residual graph
    residual = graph_to_residual(graph)
    # init node excess
    e = [0 for i in range(len(residual.nodes()))]
    stack = []
    # init distance vector
    d = [0 for i in range(len(residual.nodes()))]
    for i in residual.nodes():
        d[i] = len(nx.shortest_path(residual, source=i, target=sink))-1
    # init flow from source to neighbors
    flow_to_add = []
    for node in residual.neighbors(source):
        if d[source]>d[node]:
            r = residual[source][node]["residual"]
            flow_to_add.append(([source,node],r))
    for path,r in flow_to_add:
        add_flow_to_residual(residual,path,r)
        node = path[1]
        e[node] += r
        if e[node] > 0:
            if node not in stack:
                stack.append(node)
    # set d[source] to n
    d[source]=len(residual.nodes())
    while len(stack)!=0:
        #pop active node
        active_node = stack.pop(0)
        #print("active node = "+str(active_node))
        #find a admissible edge
        select_admissible = -1
        for nb in residual.neighbors(active_node):
            if d[active_node]>d[nb]:
                select_admissible = nb
                break
        #print("admissible neighbors = "+str(select_admissible))
        if select_admissible!=-1:
            #find min(e, r)
            resi = residual[active_node][nb]["residual"]
            current_flow = min(resi, e[active_node])
            #print("current_flow = "+str(current_flow))
            #push flow
            add_flow_to_residual(residual, [active_node,nb], current_flow)
            #update e
            e[nb] += current_flow
            if e[nb] > 0:
                if nb not in stack and nb != sink:
                    stack.append(nb)
            e[active_node] -= current_flow
            if e[active_node] > 0:
                if active_node not in stack and active_node != sink:
                    stack.append(active_node)
            #update d
            for i in residual.nodes():
                if i==source:
                    continue
                if nx.has_path(residual, source=i, target=sink):
                    d[i] = len(nx.shortest_path(residual, source=i, target=sink))-1
            #print_graph(residual)
            #print("e"+str(e))
            #print("stack"+str(stack))
            #print("d"+str(d))
        else:
            #replace d(i) by min{d(j) + 1 : (i, J) E A(i) and rli> O};
            for nb in residual.neighbors(active_node):
                r = residual[active_node][nb]["residual"]
                if r>0:
                    d[active_node] = min(d[nb]+1, r)
                    break
    #print_graph(residual)
    print(e[sink])

def add_source_sink(graph):
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
        graph.add_edge(source, node, weight=0, capacity=float("Inf"), flow=0)
    #add a new sink node that attach all sinks
    sink = len(graph.nodes()) #new node id
    for node,i in t_bag:
        graph.add_edge(node, sink, weight=0, capacity=float("Inf"), flow=0)
    return source, sink

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
