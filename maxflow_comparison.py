import networkx as nx
import matplotlib.pyplot as plt
import time
from random import randrange
#maximum flow algorithms
from algorithms.maximum_flow.generic_augmenting_path import *
from algorithms.maximum_flow.preflow_push import *
from algorithms.maximum_flow.capacity_constraint import *
from algorithms.maximum_flow.linear_programming import *
from algorithms.maximum_flow.linear_programming_cvx import *
#graph functions
from algorithms.graph_functions.api import *

###########
# DATASET #
###########

list_of_dataset = []

#generation of graph with 100 nodes
T = nx.gn_graph(100, seed=1)
G1 = nx.DiGraph()
for node_i,node_j in T.edges():
    G1.add_edge(node_j, node_i, weight=5, capacity=20, flow=0)
list_of_no_succesors = []
for node in G1.nodes():
    lenght = sum(1 for _ in G1.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G1.add_edge(node_no_succ, 100, weight=5, capacity=20, flow=0)
G1.nodes[0]['b'] = 100
G1.nodes[100]['b'] = -100
list_of_dataset.append(G1)

#generation of graph with 500 nodes
T = nx.gn_graph(500, seed=1)
G2 = nx.DiGraph()
for node_i,node_j in T.edges():
    G2.add_edge(node_j, node_i, weight=5, capacity=20, flow=0)
list_of_no_succesors = []
for node in G2.nodes():
    lenght = sum(1 for _ in G2.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G2.add_edge(node_no_succ, 500, weight=5, capacity=20, flow=0)
G2.nodes[0]['b'] = 100
G2.nodes[500]['b'] = -100
list_of_dataset.append(G2)

#generation of graph with 1000 nodes
T = nx.gn_graph(1000, seed=1)
G3 = nx.DiGraph()
for node_i,node_j in T.edges():
    G3.add_edge(node_j, node_i, weight=5, capacity=20, flow=0)
list_of_no_succesors = []
for node in G3.nodes():
    lenght = sum(1 for _ in G3.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G3.add_edge(node_no_succ, 1000, weight=5, capacity=20, flow=0)
G3.nodes[0]['b'] = 100
G3.nodes[1000]['b'] = -100
list_of_dataset.append(G3)

#generation of graph with 2500 nodes
T = nx.gn_graph(2500, seed=1)
G4 = nx.DiGraph()
for node_i,node_j in T.edges():
    G4.add_edge(node_j, node_i, weight=5, capacity=20, flow=0)
list_of_no_succesors = []
for node in G4.nodes():
    lenght = sum(1 for _ in G4.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G4.add_edge(node_no_succ, 2500, weight=5, capacity=20, flow=0)
G4.nodes[0]['b'] = 100
G4.nodes[2500]['b'] = -100
list_of_dataset.append(G4)

#generation of graph with 5000 nodes
T = nx.gn_graph(5000, seed=1)
G5 = nx.DiGraph()
for node_i,node_j in T.edges():
    G5.add_edge(node_j, node_i, weight=5, capacity=20, flow=0)
list_of_no_succesors = []
for node in G5.nodes():
    lenght = sum(1 for _ in G5.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G5.add_edge(node_no_succ, 5000, weight=5, capacity=20, flow=0)
G5.nodes[0]['b'] = 100
G5.nodes[5000]['b'] = -100
list_of_dataset.append(G5)

#generation of graph with 10000 nodes
T = nx.gn_graph(10000, seed=1)
G6 = nx.DiGraph()
for node_i,node_j in T.edges():
    G6.add_edge(node_j, node_i, weight=5, capacity=20, flow=0)
list_of_no_succesors = []
for node in G6.nodes():
    lenght = sum(1 for _ in G6.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G6.add_edge(node_no_succ, 10000, weight=5, capacity=20, flow=0)
G6.nodes[0]['b'] = 100
G6.nodes[10000]['b'] = -100
list_of_dataset.append(G6)

###############################
# Run Maximum Flow Algorithms #
###############################

###############################
# Run Maximum Flow Algorithms #
###############################

print("-- Generic augmenting path")
tab_generic = []
for i in range(len(list_of_dataset)):
    x = time.time()
    for t in range(100):
        graph, maxflow = generic_augmenting_path(list_of_dataset[i].copy())
    y = time.time()
    tab_generic.append(((y - x)/100))

print(tab_generic)

print("-- Preflow push (FIFO implementation)")
tab_preflow = []
for i in range(len(list_of_dataset)):
    x = time.time()
    for t in range(10):
        graph, maxflow = preflow_push(list_of_dataset[i].copy())
    y = time.time()
    tab_preflow.append(((y - x)/10))

print(tab_preflow)

print("-- Linear programming with an optimize simplex method")
tab_lin = []
for i in range(len(list_of_dataset)):
    x = time.time()
    for t in range(100):
        graph, maxflow = linear_programming(list_of_dataset[i].copy())
    y = time.time()
    tab_lin.append(((y - x)/100))

print(tab_lin)

print("-- Randomized short path with capacity constraint")
tab_capacity = []
for i in range(len(list_of_dataset)):
    x = time.time()
    for t in range(1):
        graph, maxflow = capacity_constraint(list_of_dataset[i].copy())
    y = time.time()
    tab_capacity.append(((y - x)/1))
    print(tab_capacity)

print(tab_capacity)

print("-- Linear programming with CVX")
tab_lin_cvx = []
for i in range(len(list_of_dataset)):
    if i==3 or i==4 or i==5: #bug for to big networks
        continue
    x = time.time()
    for t in range(100):
        graph, maxflow = linear_programming_cvx(list_of_dataset[i].copy())
    y = time.time()
    print(tab_lin_cvx)
    tab_lin_cvx.append(((y - x)/100))

print(tab_lin_cvx)

plt.plot([100, 500, 1000, 2500, 5000, 10000],tab_generic, label="generic")
plt.plot([100, 500, 1000, 2500, 5000, 10000],tab_preflow, label="preflow")
plt.plot([100, 500, 1000, 2500, 5000, 10000],tab_lin, label="lin")
plt.plot([100, 500, 1000, 2500, 5000, 10000],tab_capacity, label="capacity")
plt.plot([100, 500, 1000],tab_lin_cvx, label="lin_cvx")
plt.ylabel('time in second')
plt.xlabel('number of nodes')
plt.legend()
plt.savefig('maximumflow.png')
