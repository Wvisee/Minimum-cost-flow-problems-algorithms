from cvxopt import matrix, solvers
import numpy as np
import contextlib
from ..graph_functions.api import *

def linear_programming_cvx(graph):
    '''
    A = matrix([ [-1.0, -1.0, 0.0, 1.0], [1.0, -1.0, -1.0, -2.0] ])
    print(A)
    b = matrix([ 1.0, -2.0, 0.0, 4.0 ])
    print(b)
    c = matrix([ 2.0, 1.0 ])
    print(c)
    '''
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

    #making matrix c
    for i,j in graph.edges():
        cost = graph[i][j]["weight"]
        c[dic[str(i)+str(j)]] = float(cost)
    c = matrix(c)
    #print(c)
    #making A and b matrix edge in and out constraint
    for node in range(len(graph.nodes())):
        #adding to b
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            b.append(float(i))
            b.append(float(-i))
        else:
            b.append(0.0)
            b.append(0.0)
        #adding to A <=
        A_elem = [0.0]*var
        for child in graph.neighbors(node): #todo
            A_elem[dic[str(node)+str(child)]]=1.0
        for parent in graph.predecessors(node):
            A_elem[dic[str(parent)+str(node)]]=-1.0
        A.append(A_elem)

        #adding to A >=
        A_elem = [0.0]*var
        for child in graph.neighbors(node): #todo
            A_elem[dic[str(node)+str(child)]]=-1.0
        for parent in graph.predecessors(node):
            A_elem[dic[str(parent)+str(node)]]=1.0
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
    #print(x)
    for k in range(var):
        arr = inv_dic[k].split(" ")
        i = eval(arr[0])
        j = eval(arr[1])
        graph[i][j]["flow"] =x[k]

    cost = np.rint(compute_total_cost(graph))

    flow = 0
    for node in range(len(graph.nodes())):
        if 'b' in graph.nodes[node] and graph.nodes[node]['b'] > 0:
            flow = flow + graph.nodes[node]['b']

    return graph,flow,cost
