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
def constrainedBop_nonhitting(graph, e_g=2.0, theta=20.0):
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
    alpha, n_ref = KillingRatesForNonHittingPaths(A,sigma_in,sigma_out,e_g)
    e = e = np.ones((nr, 1))
    D = np.dot(A,e)
    D = np.zeros((nr, nr), float)
    np.fill_diagonal(D,np.dot(A,e).reshape(1,-1)[0])
    I = np.eye(nr)

    P_ref = adjacencyToTransition(A)
    diag_alpha = np.zeros((nr, nr), float)
    np.fill_diagonal(diag_alpha,alpha.reshape(1,-1)[0])
    P_ref_hat = np.dot(P_ref,(I-diag_alpha))

    W_hat = np.exp(np.dot(C,-theta)) * P_ref_hat
    Z_hat = np.linalg.solve((I - W_hat),I)

    mu_out = e
    mu_in = e
    convergence = False
    iter = 0

    while not convergence:
        mu_out_prev = mu_out
        mu_in = e/(np.dot(Z_hat,(mu_out * alpha)))
        mu_out = n_ref/(np.dot(np.transpose(Z_hat),(mu_in * sigma_in)))
        max_diff = np.absolute(mu_out_prev - mu_out).max()
        if max_diff < conv_val or iter > 10000:
            convergence = True
        iter = iter + 1

    #print(mu_in)
    #print(mu_out)

    #N_exp = diag(n_ref ./ mu_out) * W_hat * (diag(mu_in)\I)
    diag_mu_in = np.zeros((nr, nr), float)
    np.fill_diagonal(diag_mu_in,mu_in.reshape(-1,1))
    diag_mu_out = np.zeros((nr, nr), float)
    np.fill_diagonal(diag_mu_out,(n_ref/mu_out).reshape(-1,1))
    N_exp = np.dot((np.dot(diag_mu_out,W_hat)),(np.linalg.solve(diag_mu_in,I)))

    for i in range(nr):
        for j in range(nc):
            if N_exp[i][j]<0.0000001:
                N_exp[i][j]=0

    adj_flow = N_exp_to_flow(N_exp,in_counter)

    flow = in_counter

    for i in range(nr):
        for j in range(nc):
            if adj_flow[i][j]>0:
                graph[i][j]["flow"]= adj_flow[i][j]

    cost = compute_total_cost(graph)

    return graph, flow, cost

def N_exp_to_flow(N_exp,in_counter):
    return np.rint(N_exp*in_counter)

def adjacencyToTransition(A):
    nr = len(A[0])
    nc = len(A[0])
    e  = np.ones((nr, 1))

    s = np.sum(A, axis=1).reshape(-1,1)#sum of each row
    P = np.divide(A,(np.ones((nr, nr)) * s))
    P = np.nan_to_num(P, nan=0.0)
    return P

def KillingRatesForNonHittingPaths(A,sigma_in,sigma_out,e_g):
    nr = len(A[0])
    I = np.eye(nr)
    P_ref = adjacencyToTransition(A)
    Q = I - np.transpose(P_ref)
    pinv_Q = np.linalg.pinv(Q)
    q = (I - np.dot(pinv_Q,Q))
    q = q[0].reshape(-1,1)

    n_ref_zero = np.dot(pinv_Q,(np.dot((sigma_in - np.transpose(P_ref)),sigma_out)))
    epsillon = ((sigma_out - n_ref_zero)/q).max() + e_g
    n_ref = n_ref_zero + np.dot(epsillon,q)
    alpha = np.divide(sigma_out,n_ref)
    alpha = np.nan_to_num(alpha, nan=0.0)

    return alpha, n_ref
