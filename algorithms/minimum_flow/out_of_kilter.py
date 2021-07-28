import networkx as nx
from ..maximum_flow.generic_augmenting_path import *
from ..graph_functions.api import *
import sys

'''
This algorithms has been based on the following document
Journal of the Society for Industrial and Applied Mathematics , Mar., 1961, Vol.9, No. 1 (Mar., 1961), pp. 18-27
Author(s): D. R. Fulkerson
'''

def out_of_kilter(graph):
    #find sinks and sources
    source, sink = add_source_sink_mincost(graph)
    #set potentials
    pi = [0 for i in range(len(graph.nodes()))]
    #find a feasible solution
    graph, maxflow = generic_augmenting_path(graph)
    #print_graph(graph)
    #compute kilter number
    kilter_number = {}
    for s,t in graph.edges():
        x = get_kilter_number(graph,(s,t),pi)
        kilter_number[(s,t)] = x

    number, edge = get_out_of_kilter_edge(kilter_number) #if no out-of-kilter return -1
    forced_bag = []

    while number>0:
        #print("edge = "+str(edge)+" / number = "+str(number))
        s = edge[0]
        t = edge[1]
        weight = graph[s][t]["weight"]
        flow = graph[s][t]["flow"]
        capacity = graph[s][t]["capacity"]
        C_pi_st = weight + pi[s] - pi[t]

        if (C_pi_st>0 and flow<0) or (C_pi_st==0 and flow<0) or (C_pi_st<0 and flow<capacity):
            #source = t, destination = s
            origin = t
            terminal = s
        elif (C_pi_st>0 and flow>0) or (C_pi_st==0 and flow>capacity) or (C_pi_st<0 and flow>capacity):
            #source = t, destination = s
            origin = s
            terminal = t

        while kilter_number[(s,t)]!=0:
            #find path
            #print("find path from :"+str((s,t)))
            #print(C_pi_st)
            #print(pi)
            path, amount = find_path(origin,terminal,graph,pi,C_pi_st)
            if path==[]:
                #non-breakthrough
                #print("non-breakthrough")
                is_sigma_infinity = add_sigma_to_pi(graph, pi)
                if is_sigma_infinity:
                    #change out of kilter edge because no feasible circulation
                    forced_bag.append(edge)
                    break
            else:
                #breakthrough
                add_flow_to_graph(graph,path,amount)
                #update kilter number
                for u,v in graph.edges():
                    x = get_kilter_number(graph,(u,v),pi)
                    kilter_number[(u,v)] = x

                #print_graph(graph)
                #print(compute_total_cost(graph))
                break

        number, edge = get_out_of_kilter_edge(kilter_number, forced_bag)

    #get flow
    flow = 0
    for node in graph.neighbors(source):
        flow += graph[source][node]["flow"]
    #delete virtual edge that connect multiple source and sink
    remove_source_sink(graph, source, sink)
    #compute total cost of flow
    total_cost = compute_total_cost(graph)
    #return solution
    return graph, flow, total_cost

#find a path from origin to terminal with the labeling technics
#return the path if founded, else return empty path
def find_path(origin,terminal,graph,pi,C_pi_st):
    #delete previous label
    for node in graph.nodes():
        if 'label' in graph.nodes[node]:
            del graph.nodes[node]['label']
    #found path variable
    found = False
    #labeling phase
    graph.nodes[origin]['label'] = [len(graph.nodes()),None,float("Inf")]
    stack = [origin]
    for i in stack:
        #print(str(i))
        for j in graph.neighbors(i):
            #print("Forward")
            if i==origin and j==terminal:
                continue
            if 'label' not in graph.nodes[j]:
                weight = graph[i][j]["weight"]
                flow = graph[i][j]["flow"]
                capacity = graph[i][j]["capacity"]
                C_pi_ij = weight + pi[i] - pi[j]
                if C_pi_ij>0 and flow<0:
                    #print("label node : "+str(j))
                    ei = graph.nodes[i]['label'][2]
                    ej = min(ei,-flow) #-flow
                    #print("label = "+str([i,True,ej]))
                    graph.nodes[j]['label'] = [i,True,ej]
                    stack.append(j)
                elif C_pi_ij<=0 and flow<capacity:
                    #print("label node : "+str(j))
                    ei = graph.nodes[i]['label'][2]
                    ej = min(ei,capacity-flow)
                    #print("label = "+str([i,True,ej]))
                    graph.nodes[j]['label'] = [i,True,ej]
                    stack.append(j)
        for j in graph.predecessors(i):
            #print("Backward")
            if j==origin and i==terminal: #a mon avis jamais tombé dedans
                continue
            if 'label' not in graph.nodes[j]:
                weight = graph[j][i]["weight"]
                flow = graph[j][i]["flow"]
                capacity = graph[j][i]["capacity"]
                C_pi_ji = weight + pi[j] - pi[i]
                if C_pi_ji>=0 and flow>0:
                    #print("label node : "+str(j))
                    ei = graph.nodes[i]['label'][2]
                    ej = min(ei,flow)
                    #print("label = "+str([i,False,ej]))
                    graph.nodes[j]['label'] = [i,False,ej]
                    stack.append(j)
                elif C_pi_ji<0 and flow>capacity:
                    #print("label node : "+str(j))
                    ei = graph.nodes[i]['label'][2]
                    ej = min(ei,flow-capacity)
                    #print("label = "+str([i,False,ej]))
                    graph.nodes[j]['label'] = [i,False,ej]
                    stack.append(j)
        if terminal in stack:
            found = True
            break
    if found:
        #print("found")
        #print_graph_label(graph)
        #get amount
        if not graph.has_edge(origin,terminal):
            s = terminal
            t = origin
        else:
            s = origin
            t = terminal

        flow = graph[s][t]["flow"]
        capacity = graph[s][t]["capacity"]
        if C_pi_st>0 and flow<0:
            path_amount = graph.nodes[s]['label'][2]
            amount = min(path_amount,-flow) #-flow
        elif (C_pi_st==0 and flow<0) or (C_pi_st<0 and flow<capacity):
            path_amount = graph.nodes[s]['label'][2]
            amount = min(path_amount,capacity-flow)
        elif (C_pi_st>0 and flow>0) or (C_pi_st==0 and flow>capacity):
            path_amount = graph.nodes[t]['label'][2]
            amount = min(path_amount,flow)
        elif C_pi_st<0 and flow>capacity:
            path_amount = graph.nodes[t]['label'][2]
            amount = min(path_amount,flow-capacity)
        #print("amount = "+str(amount))
        #get path
        path = []
        current = terminal
        stop = False
        while not stop:
            if current==origin:
                stop = True
                if graph.nodes[current]['label'][1]==None:
                    if C_pi_st>0:
                        path.append((current,False))
                    elif C_pi_st<0:
                        path.append((current,True))
                else:
                    path.append((current,graph.nodes[current]['label'][1]))
                path.append((terminal,None))
            else:
                path.append((current,graph.nodes[current]['label'][1]))
                current = graph.nodes[current]['label'][0]
        #print("Path = "+str(path))
        #return path
        return path, amount
    else:
        #print("not found")
        return [],0

#compute sigma and add it to all the pi of unlabel nodes
#if sigma is infinite then return True and don't update pi
def add_sigma_to_pi(graph,pi):
    #label to unlabel find cij>0, xij <= uij
    a1 = []
    #unlabel to label cij <0, xij >=0
    a2 = []
    #compute a1 and a2
    for i, j in graph.edges():
        weight = graph[i][j]["weight"]
        flow = graph[i][j]["flow"]
        capacity = graph[i][j]["capacity"]
        C_pi_ij = weight + pi[i] - pi[j]
        if 'label' in graph.nodes[i] and not 'label' in graph.nodes[j]:
            if C_pi_ij>0 and flow<=capacity:
                a1.append((i,j,C_pi_ij))
        elif not 'label' in graph.nodes[i] and 'label' in graph.nodes[j]:
            if C_pi_ij<0 and flow>=0:
                a2.append((i,j,C_pi_ij))
    if len(a1)==0 and len(a2)==0:
        return True
    #min of all cij in a1 => if empty => infini
    sigma_a1 = sys.maxsize
    for i,j,c in a1:
        if c<sigma_a1:
            sigma_a1=c
    #min of all - cij in a2 => if empty => infini
    sigma_a2 = sys.maxsize
    for i,j,c in a2:
        if -c<sigma_a2:
            sigma_a2 = -c
    #computation of sigma
    sigma = min(sigma_a1,sigma_a2)
    #print("sigma : "+str(sigma))
    #add sigma to all pi i in unlabel
    for i in graph.nodes():
        if not 'label' in graph.nodes[i]:
            pi[i] += sigma
    return False

#add flow to a graph (not a residual graph)
def add_flow_to_graph(graph,path,amount):
    for i in range(len(path)-1):
        u = path[i][0]
        cond_u = path[i][1]
        v = path[i+1][0]
        if cond_u:
            graph[v][u]["flow"] += amount
        else:
            graph[u][v]["flow"] -= amount

#find the kilter number of the edge
def get_kilter_number(graph, edge, pi):
    u = edge[0]
    v = edge[1]

    flow = graph[u][v]["flow"]
    capacity = graph[u][v]["capacity"]
    weight = graph[u][v]["weight"]

    C_pi_uv = weight + pi[u] - pi[v]

    if C_pi_uv>0:
        if flow==0:
            return 0
        else: #flow>0
            return flow
    elif C_pi_uv==0:
        if 0<=flow<=capacity:
            return 0
    else: #C_pi_uv<0
        if flow==capacity:
            return 0
        else:
            return capacity-flow

#return biggest kilter number edge
def get_out_of_kilter_edge(kilter_number, forced_bag = []):
    max = 0
    edge = (0,0)
    for i in kilter_number:
        if i not in forced_bag:
            number = kilter_number[i]
            if number>max:
                max = number
                edge = i
    if max==0:
        return -1, (0,0) #if no out of kilter
    else:
        return max, edge

#print the label of all nodes in the graph
def print_graph_label(graph):
    for i in graph.nodes():
        if 'label' in graph.nodes[i]:
            print("node:"+str(i)+" => label:"+str(graph.nodes[i]['label']))
