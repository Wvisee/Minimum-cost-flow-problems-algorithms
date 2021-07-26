from ..graph_functions.api import *
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import math
import networkx as nx
import scipy as sp #for adjacency_matrix
'''
This code is the transformation of the capacity_contraint hitting written in MatLab
into python3 code.
It is the second algorithm of the paper
Theta must lie between 0.00000001 and 20.0
'''
def capacity_constraint(graph, theta=2):
    #link all source and sink to a single node source and a single node sink
    source, sink = add_source_sink_maxflow_rsp_with_constraint(graph)

    #Initialisation
    nr = len(graph.nodes()) #because size() in mathlab return the size of matrix
    nc = len(graph.nodes()) #matrix is same width than length

    mini = 1000000*float("2.2251e-308") #taken from matlab realmin
    maxi = float("1.7977e+308")/1000000 #taken from matlab realmax
    eps = float("1e-10")

    #sparse matrix is a matrix with a lot of 0
    #full matrix is when we store (u,v) = x and we ommit the 0
    #A = np.zeros((nr,nc))
    C0 = np.full((nr,nc), maxi)
    for u,v in graph.edges():
        C0[u][v]=1
    C0[source][sink] = 10

    #nargin is the number of argument of the function => maintained in def signature
    S = np.zeros((nr,nc))
    for u,v in graph.edges():
        capacity = graph[u][v]["capacity"]
        S[u][v]=capacity

    '''
    source = 0
    sink = 9

    nr = 10
    nc = 10

    C0  = [[maxi,1,1,1,maxi,maxi,maxi,maxi,maxi,10],
                [1,maxi,1,maxi,1,maxi,maxi,maxi,maxi,maxi],
                [1,1,maxi,maxi,1,1,maxi,maxi,maxi,maxi],
                [1,maxi,maxi,maxi,maxi,1,maxi,maxi,maxi,maxi],
                [maxi,1,1,maxi,maxi,maxi,1,1,1,maxi],
                [maxi,maxi,1,1,maxi,maxi,maxi,maxi,1,maxi],
                [maxi,maxi,maxi,maxi,1,maxi,maxi,1,maxi,1],
                [maxi,maxi,maxi,maxi,1,maxi,1,maxi,maxi,1],
                [maxi,maxi,maxi,maxi,1,1,maxi,maxi,maxi,1],
                [maxi,maxi,maxi,maxi,maxi,maxi,1,1,1,maxi]]

    S = np.zeros((nr,nc))
    S[0][1] = 4
    S[0][2] = 7
    S[0][3] = 7
    S[1][2] = 5
    S[1][4] = 2
    S[2][4] = 6
    S[2][5] = 3
    S[3][5] = 1
    S[4][6] = 4
    S[4][7] = 7
    S[4][8] = 4
    S[5][8] = 10
    S[6][9] = 1
    S[6][7] = 2
    S[7][9] = 10
    S[8][9] = 11

    S = S + np.transpose(S)
    '''

    sum_source_s = 0
    for i in range(len(S)):
        sum_source_s = sum_source_s + S[source][i]
    sum_sink_s = 0
    for i in range(len(S)):
        sum_sink_s = sum_sink_s + S[sink][i]
    TotalCap = max(sum_source_s,sum_sink_s)
    S = S/TotalCap

    P0 = costToPtrans01(C0, eps, nr)

    struct1 = inequalityConstraintCapacity03(C0,P0,source,sink,S,theta)

    PassageReel = np.dot(struct1["ArcPassages"],TotalCap)

    Maxflow = 0
    for i in range(len(PassageReel)):
        Maxflow = Maxflow + PassageReel[i][sink]
    Maxflow = Maxflow - PassageReel[source][sink]

    adj_flow = np.rint(PassageReel)
    #print_matrix(adj_flow)

    remove_source_sink(graph, source, sink)

    for i in range(nr-2): #-2 because we delete the source and sink that were linked the multiple source and sink
        for j in range(nc-2):
            if adj_flow[i][j]>0:
                graph[i][j]["flow"]= adj_flow[i][j]

    return graph,np.rint(Maxflow)

def costToPtrans01(C0, eps, nr):
    A = np.zeros((nr,nr))
    for i in range(len(C0)):
        for j in range(len(C0[0])):
            if C0[i][j]>=eps:
                A[i][j]=1/C0[i][j]
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j]<eps:
                A[i][j]=0
    for i in range(len(A)):
        for j in range(len(A[0])):
            if A[i][j]>eps:
                A[i][j]=1

    e = np.ones((nr, 1))
    P0 = A
    Den = np.sum(P0, axis=1).reshape(-1,1)*np.transpose(e)
    for i in range(len(P0)):
        for j in range(len(P0[0])):
            if P0[i][j]<eps:
                P0[i][j]=0
            elif Den[i][j]>=eps:
                P0[i][j] = P0[i][j]/Den[i][j]
    return P0

def inequalityConstraintCapacity03(C,P,source,sink,S,theta):
    alpha = 1/theta
    n = len(C)

    constraintsList_x, constraintsList_y = np.nonzero(S > 0)

    lamda = np.zeros((n,n)) #lamda and not lambda because keyword already used
    Cext = np.copy(C)

    dualLagrangeFunction = []
    l = 0
    l_1 = -1

    iteration = 0
    while (np.abs(l - l_1) > 0.00001) and (iteration <=500):
        struct1 = rspKullbackPref01(Cext,P,theta,source,sink)

        N = struct1["ArcPassages"]
        z1 = struct1["OriginFundamentalMatrix"]
        zp = z1[n-1][0]

        l_1 = 1
        l = - math.log(zp)/theta
        dualLagrangeFunction = np.hstack((dualLagrangeFunction,l))

        for i,j in zip(constraintsList_x, constraintsList_y):
            lamda[i][j] = max(lamda[i][j] + np.dot((2*alpha),(N[i][j] - S[i][j])), 0)
            Cext[i][j] = C[i][j] + lamda[i][j]


        iteration = iteration + 1

    return rspKullbackPref01(Cext,P,theta,source,sink)

def rspKullbackPref01(C0,P0,theta,i,j):
    eps = 1000000*float("2.2251e-308") #taken from matlab realmin

    MEstruct = {}
    MEstruct["cost"] = 0
    MEstruct["ArcPassages"] = 0
    MEstruct["NodePassages"] = 0
    MEstruct["TransitionsProba"] = 0
    MEstruct["entropy"] = 0

    nr = len(C0)
    nc = len(C0[0])

    e = np.ones((nr, 1))
    I = np.eye(nr)

    W = np.exp(np.dot(C0,-theta))*P0

    Ij = I.copy()
    Ij[j][j] = 0
    Wj = np.dot(Ij,W)

    ei = I[:,i].reshape(-1,1)
    ej = I[:,j].reshape(-1,1)

    zci = np.linalg.solve(np.transpose(I - Wj), ei)
    zcj = np.linalg.solve((I - Wj), ej)
    zcij = np.dot(np.transpose(ei),zcj)

    x = (C0 * Wj)
    x = np.nan_to_num(x, nan=0.0)
    dij = np.divide(np.dot(np.dot(np.transpose(zci),x),zcj),zcij)

    diag_zci = np.zeros((nr, nr), float)
    np.fill_diagonal(diag_zci,zci.reshape(1,-1)[0])
    diag_zcj = np.zeros((nr, nr), float)
    np.fill_diagonal(diag_zcj,zcj.reshape(1,-1)[0])
    N = np.divide(np.dot(np.dot(diag_zci,Wj),diag_zcj),zcij)

    n = np.sum(N, axis=1).reshape(-1,1)

    Den = np.dot(n,np.transpose(e))
    P = np.zeros((nr, nc))
    for i in range(len(P)):
        for j in range(len(P[0])):
            if N[i][j]>eps:
                P[i][j]= N[i][j]/Den[i][j]
            else:
                P[i][j] = 0

    ent = -(math.log(zcij) + theta * dij)

    MEstruct["cost"] = dij
    MEstruct["ArcPassages"] = N
    MEstruct["NodePassages"] = n
    MEstruct["TransitionsProba"] = P
    MEstruct["entropy"] = ent
    MEstruct["OriginFundamentalMatrix"] = zci
    MEstruct["DestinationFundamentalMatrix"] = zcj

    return MEstruct

def print_matrix(A):
    for i in range(len(A)):
        for j in range(len(A[0])):
            print(str(A[i,j])+" ", end='')
        print("")
