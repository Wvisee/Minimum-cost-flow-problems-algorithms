from cvxopt import matrix, solvers
import numpy as np
import contextlib
from ..graph_functions.api import *

def linear_programming_cvx(graph):

    source, sink = add_source_sink_maxflow_rsp_with_constraint(graph)
    #source, sink = get_source_sink(graph)
    graph.add_edge(sink, source, weight=0, capacity=100000, flow=0)

    #creating a number for each edge to reconize them
    dic = {}
    inv_dic = {}
    var = 0
    for i,j in graph.edges():
        dic[str(i)+str(j)]=var
        inv_dic[var]=str(i)+" "+str(j)
        var = var + 1

    #adding attribute into matrix
    A = []
    b = []
    c = [0.0]*var

    #making c
    c[dic[str(sink)+str(source)]]=-1.0
    c = matrix(c)
    #print(c)
    #making A and b matrix edge in and out constraint
    for node in range(len(graph.nodes())):
        b.append(0.0)
        b.append(0.0)
        #adding to A <=
        A_elem = [0.0]*var
        for child in graph.neighbors(node): #todo
            A_elem[dic[str(node)+str(child)]]=-1.0
        for parent in graph.predecessors(node):
            A_elem[dic[str(parent)+str(node)]]=1.0
        A.append(A_elem)
        #adding to A >=
        A_elem = [0.0]*var
        for child in graph.neighbors(node): #todo
            A_elem[dic[str(node)+str(child)]]=1.0
        for parent in graph.predecessors(node):
            A_elem[dic[str(parent)+str(node)]]=-1.0
        A.append(A_elem)

    #adding capacity constraint
    for i,j in graph.edges():
        capacity = graph[i][j]["capacity"]
        #xij <= capij
        b.append(capacity)
        A_elem = [0.0]*var
        A_elem[dic[str(i)+str(j)]]=1.0
        A.append(A_elem)
        #xij >= 0
        b.append(0.0)
        A_elem = [0.0]*var
        A_elem[dic[str(i)+str(j)]]=-1.0
        A.append(A_elem)

    numpy_array = np.array(A)
    transpose = numpy_array.T
    A = transpose.tolist()
    #making A and b matrix capactity constraint

    A = matrix(A)
    #print(A)
    b = matrix(b)
    #print(b)

    with contextlib.redirect_stdout(None):
        sol=solvers.lp(c,A,b)

    x = sol['x']
    for i in range(len(x)):
        if x[i]<0.0000001:
            x[i]=0

    maxflow=round(x[-1])

    return graph,maxflow
