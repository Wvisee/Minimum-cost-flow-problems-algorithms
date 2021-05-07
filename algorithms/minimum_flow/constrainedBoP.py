import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import math
import networkx as nx
import scipy as sp #for adjacency_matrix
'''
This code is the transformation of the constrainedBoP written in MatLab
into python3 code

theta must lie between 0.00000001 and 20.0
absorbing => True then hitting paths are considered
          => False non-hitting paths are considered
'''
def constrainedBop(graph, theta, absorbing=False):
    #Initialisation
    nr = len(graph.nodes()) #because size() in mathlab return the size of matrix
    nc = len(graph.nodes()) #matrix is same width than length

    eps = 1000*float("2.2251e-308") #taken from matlab realmin
    myMax = float("1.7977e+308") #taken from matlab realmax
    conv_val = float("1e-6")

    #don't really need as we don't store graph as adjacency matrix
    if nr!=nc:
        print("Error: The cost matrix is not square !")
        return

    #sparse matrix is a matrix with a lot of 0
    #full matrix is when we store (u,v) = x and we ommit the 0
    A0 = nx.to_numpy_array(graph)

    #nargin is the number of argument of the function => maintained in def signature
    weights = np.ones((nr,1))/nr

    #Algorithm
    e = np.ones((nr, nr))/nr
    I = np.eye(nr)
    H = I - e

    #Computation of the cost matrix C
    C = nx.to_numpy_array(graph)
    for i in range(len(C)):
        for j in range(len(C[i])):
            if A0[i,j] >= eps:
                C[i][j] = float(1.0/A0[i,j])
            else:
                C[i][j] = myMax
    for i in range(len(A0)):
        for j in range(len(A0)):
            if A0[i,j] < eps:
                A0[i,j] = 0

    # Computation of P, the reference transition probabilities matrix
    # representing the natural random walk on the graph
    s = np.sum(A0, axis=1).reshape(-1,1)#sum of each row
    P = np.divide(A0,(np.ones((nr, nr)) * s))

    # sigma_in as weight
    s_in = weights
    s_out = weights

    # Construction of the diffents elements which depends on absorbing option
    if absorbing:
        #matrices W and Z, vectors divisor and out_val
        W = np.multiply(np.exp(np.dot(C,-theta)),P)
        Z = np.linalg.solve((I - W),I)
        divisor = np.diag(Z).reshape(-1,1)
        numerator = np.diag(Z).reshape(-1,1) ###!!!Maybe loss of litle data 1.000 instead of 1.00000005555 by ex
        out_val = s_out
    else:
        #construction of alpha and n_ref
        Q = I - np.transpose(P)
        pinv_Q = np.linalg.pinv(Q)
        q = (I - np.dot(pinv_Q,Q))
        q = q[:,1].reshape(-1,1)

        n_ref_0 = np.dot(pinv_Q,(np.dot((s_in - np.transpose(P)),s_out)))
        gamma = ((s_out - n_ref_0)/q).max() + 1
        n_ref = n_ref_0 + np.dot(gamma,q)
        alpha = np.divide(s_out,n_ref)
        X = alpha.reshape(1,-1)[0]
        P_mod = np.dot((I - np.diag(X)),P)

        #matrices W and Z, vectors divisor and out_val
        W = np.multiply(np.exp(np.dot(C,-theta)),P_mod)
        Z = np.linalg.solve((I - W),I)
        divisor = np.ones((nr,1))
        numerator = n_ref
        out_val = alpha

    m_in = np.ones((nr, 1))
    m_out = np.ones((nr, 1))
    convergence = False
    iter = 0
    while not convergence:
        m_out_prev = m_out
        L = np.multiply(m_out,out_val)
        m_in = np.divide(np.ones((nr, 1)),(np.dot(Z,(np.divide(L,divisor)))))
        m_out = np.divide(numerator,(np.dot(np.transpose(Z),np.multiply(m_in,s_in))))
        max_diff = np.absolute(m_out_prev - m_out).max()
        if max_diff < conv_val or iter > 10000:
            convergence = True
        iter = iter + 1

    sub_Pi_SBOP = np.dot(np.diag(np.multiply(m_in,s_in).reshape(1,-1)[0]),Z)
    Pi_CBOP = np.dot(sub_Pi_SBOP,np.diag(np.divide(np.multiply(m_out,out_val),divisor).reshape(1,-1)[0]))

    #var declaration
    D_CBOP = np.divide(np.dot((np.log(Pi_CBOP) + np.log(np.transpose(Pi_CBOP))),-1),2)
    D_CBOP = D_CBOP - np.diag(np.diag(D_CBOP))

    for i in range(len(D_CBOP)):
        for j in range(len(D_CBOP[i])):
            sub_d_cbop = myMax/(nr*(nr-1))
            if D_CBOP[i,j] > sub_d_cbop:
                D_CBOP[i][j] = sub_d_cbop
    for i in range(len(D_CBOP)):
        for j in range(len(D_CBOP[i])):
            if D_CBOP[i,j] == float("Inf"):
                D_CBOP[i][j] = myMax/(nr*(nr-1))

    #Gaussian kernel from the CBOP distance
    a = 1
    D2 = np.multiply(D_CBOP,D_CBOP)
    sig = np.divide(np.sum(np.sum(D2)),(nr*(nr-1)))
    Krg = np.exp(np.divide(np.dot(-a,D2),sig))
    Krg = np.divide((Krg + np.transpose(Krg)),2)
    Krg = np.real(Krg)
    Lam, U = np.linalg.eig(Krg)
    #change >= to > because not correct in python
    if np.not_equal(np.sum(np.diag(Lam) >0),nr):
        Lam = max(Lam.real,0)
        U = U.real
        Krg = np.dot(np.dot(U,Lam),np.transpose(U))
        Krg = np.divide((Krg + np.transpose(Krg)),2)
        Krg = Krg.real

    #MDS kernel from the CBOP distance
    Ks = np.dot(H,np.transpose(np.dot(H,np.multiply(D_CBOP,D_CBOP)))) * -0.5
    Ks = np.divide((Ks + np.transpose(Ks)),2)
    Ks = np.real(Ks)
    Lam, U = np.linalg.eig(Ks)
    if np.not_equal(np.sum(np.diag(Lam) >0),nr):
        Lam = np.diag(np.maximum(Lam.real,0))
        U = U.real
        Ks = np.dot(np.dot(U,Lam),np.transpose(U))
        Ks = np.divide((Ks + np.transpose(Ks)),2)
        Ks = Ks.real

    print(D_CBOP)
    print(Krg)
    print(Ks)

    #return result
    return D_CBOP,Krg,Ks
