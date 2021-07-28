from ..graph_functions.api import *
import networkx as nx
import sys

#weight and capacity must not equal to 0
def preflow_push(graph):

    connect_all_source_or_sink = False
    if multiple_source_or_sink(graph):
        # add one source and one sink that connect multiple source and sink
        source, sink = add_source_sink_maxflow(graph)
        connect_all_source_or_sink = True
    else:
        source, sink = get_source_sink(graph)

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
        '''
        print("d = "+str(d))
        print("e = "+str(e))
        print_graph(residual)
        '''
        #pop active node
        active_node = stack.pop(0)
        '''
        print("active_node = "+str(active_node))
        '''
        #find a admissible edge
        select_admissible = findadmissible(residual,active_node, d)
        '''
        print("admissible neighbors = "+str(select_admissible))
        '''
        if select_admissible!=-1:
            #find min(e, r)
            resi = residual[active_node][select_admissible]["residual"]
            current_flow = min(resi, e[active_node])
            #print("current_flow = "+str(current_flow))
            #push flow
            add_flow_to_residual(residual, [active_node,select_admissible], current_flow)
            #update e
            if select_admissible!=source:
                e[select_admissible] += current_flow
            if e[select_admissible] > 0:
                if select_admissible not in stack and select_admissible != sink:
                    stack.append(select_admissible)
            e[active_node] -= current_flow
            if e[active_node] > 0:
                if active_node not in stack and active_node != sink:
                    stack.append(active_node)
            #'''
            #update d
            for i in residual.nodes():
                if i==source:
                    continue
                if nx.has_path(residual, source=i, target=sink):
                    d[i] = len(nx.shortest_path(residual, source=i, target=sink))-1
            #'''
            #print_graph(residual)
            #print("e"+str(e))
            #print("stack"+str(stack))
            #print("d"+str(d))
        else:
            #replace d(i) by min{d(j) + 1 : (i, j) e A(i) and rij> O};
            min_d = float("Inf")
            for nb in residual.neighbors(active_node):
                if min_d>d[nb]:
                    min_d = d[nb]
            d[active_node] = min_d + 1
            stack.append(active_node)
    #get maxflow
    maxflow = e[sink]

    if connect_all_source_or_sink:
        #delete virtual edge that connect multiple source and sink
        remove_source_sink(residual, source, sink)

    #residual to graph
    graph = residual_to_graph(residual)
    return graph, maxflow

def findadmissible(residual, active_node, d):
    select_admissible = -1                          #update here need to add residual check and loop through all => delete break must help
    for nb in residual.neighbors(active_node):
        if d[active_node]>d[nb]:
            select_admissible = nb
            break
    return select_admissible
