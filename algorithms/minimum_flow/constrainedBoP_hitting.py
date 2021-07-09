from ..graph_functions.api import *
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import math
import networkx as nx
import scipy as sp #for adjacency_matrix
'''
This code is the transformation of the constrainedBoP hitting written in MatLab
into python3 code
It is the third algorithm of the paper
Theta must lie between 0.00000001 and 20.0
'''
def constrainedBop_hitting(graph, theta=20.0):
    #Initialisation
    nr = len(graph.nodes()) #because size() in mathlab return the size of matrix
    nc = len(graph.nodes()) #matrix is same width than length

    #Set sigma_in and sigma_out representing the demand and offer
    sigma_in = np.zeros((nr, 1), dtype=float)
    sigma_out = np.zeros((nr, 1), dtype=float)
    in_counter = 0
    out_counter = 0
    for node in graph.nodes():
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            if i < 0: #demand
                out_counter += -i
                sigma_out[node][0] = -i
            elif i > 0: #offer
                in_counter += i
                sigma_in[node][0] = i
    for i in range(len(sigma_in)):
        sigma_in[i][0] = sigma_in[i][0]/in_counter
    for i in range(len(sigma_out)):
        sigma_out[i][0] = sigma_out[i][0]/out_counter

    eps = 1000*float("2.2251e-308") #taken from matlab realmin
    myMax = float("1.7977e+308") #taken from matlab realmax
    conv_val = float("1e-6")

    #sparse matrix is a matrix with a lot of 0
    #full matrix is when we store (u,v) = x and we ommit the 0
    A = np.zeros((nr,nc))
    for u,v in graph.edges():
        A[u][v]=1

    #nargin is the number of argument of the function => maintained in def signature
    C = np.zeros((nr,nc))
    for u,v in graph.edges():
        weight = graph[u][v]["weight"]
        C[u][v]=weight

    #Algorithm
    e = np.ones((nr, 1))
    I = np.eye(nr)
    D = np.dot(A,e)
    D = np.zeros((nr, nr), float)
    np.fill_diagonal(D,np.dot(A,e).reshape(1,-1)[0])

    InvD = np.divide(I,D)
    InvD = np.nan_to_num(InvD, nan=0.0)

    P_ref = np.dot(InvD,A)

    W = np.multiply(np.exp(np.dot(C,-theta)),P_ref)
    #Z = np.linalg.solve((I - W),I)
    Z = np.linalg.solve((I - W),I)
    #Z = np.nan_to_num(Z, nan=0.0)
    D_h = np.zeros((nr, nr), float)
    np.fill_diagonal(D_h,np.diag(Z).reshape(-1,1))
    x = np.linalg.solve(D_h,I)
    #x = np.nan_to_num(x, nan=0.0)
    Z_h = Z @ x

    mu_out_h = e
    mu_in_h = e

    oldmu_out_h = np.zeros((nr, 1), float)
    oldmu_in_h = np.zeros((nr, 1), float)
    while (np.sum(np.divide(np.abs(mu_in_h - oldmu_in_h),nr)) > 0.00001) or (np.sum(np.divide(np.abs(mu_out_h - oldmu_out_h),nr)) > 0.00001):
        oldmu_out_h = mu_out_h
        oldmu_in_h = mu_in_h

        mu_in_h = e/np.dot(Z_h,(mu_out_h*sigma_out))
        mu_out_h = e/np.dot(np.transpose(Z_h),(mu_in_h * sigma_in))
    #N_exp_h = ((e ./ mu_out_h)*(e ./ mu_in_h)' - (Z_h*diag(sigma_out)*Z_h)') .* (diag(diag(Z))*W);
    diag_sigma_out = np.zeros((nr, nr), float)
    np.fill_diagonal(diag_sigma_out,np.diag(sigma_out).reshape(-1,1))
    N_exp_h = (np.dot((e/mu_out_h),np.transpose((e/mu_in_h))) -  np.transpose(np.dot(np.dot(Z_h,diag_sigma_out),Z_h)))  * np.dot(np.diag(np.diag(Z)),W)
    for i in range(nr):
        for j in range(nc):
            if N_exp_h[i][j]<0.0000001:
                N_exp_h[i][j]=0

    #print(N_exp_h)

    adj_flow = N_exp_h_to_flow(N_exp_h,in_counter)
    #print(adj_flow)

    flow = in_counter

    for i in range(nr):
        for j in range(nc):
            if adj_flow[i][j]>0:
                graph[i][j]["flow"]= adj_flow[i][j]

    cost = compute_total_cost(graph)

    return graph, flow, cost

def N_exp_h_to_flow(N_exp_h,in_counter):
    return np.rint(N_exp_h*in_counter)
