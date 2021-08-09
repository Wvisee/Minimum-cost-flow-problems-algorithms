import networkx as nx
import matplotlib.pyplot as plt
import time
from random import randrange
#randomized optimal flow algorithms
from algorithms.minimum_flow.constrainedBoP_hitting import *
from algorithms.minimum_flow.constrainedBoP_nonhitting import *
from algorithms.maximum_flow.capacity_constraint import *
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

####################################
# Randomized algorithms comparison #
####################################

theta_tab = [0.01, 0.1, 1, 2, 5, 10, 20]

print("-- Constrained hitting bag-of-paths")
total_tab = []
for theta_val in theta_tab:
    print(theta_val)
    tab_hitting = []
    for i in range(len(list_of_dataset)):
        x = time.time()
        cost = 0
        for t in range(10):
            graph, flow, cost = constrainedBop_hitting(list_of_dataset[i].copy(), theta=theta_val)
        print(cost)
        y = time.time()
        tab_hitting.append(((y - x)/10))
    total_tab.append(tab_hitting)

plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[0], label="0.01")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[1], label="0.1")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[2], label="1")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[3], label="2")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[4], label="5")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[5], label="10")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[6], label="20")
plt.ylabel('time in seconds')
plt.xlabel('number of nodes')
plt.legend()
plt.savefig('hitting_bop.png')
plt.clf()

print("-- Constrained non-hitting bag-of-paths")
total_tab = []
for theta_val in theta_tab:
    print(theta_val)
    tab_nonhitting = []
    for i in range(len(list_of_dataset)):
        x = time.time()
        cost = 0
        for t in range(10):
            graph, flow, cost = constrainedBop_nonhitting(list_of_dataset[i].copy(), theta=theta_val)
        print(cost)
        y = time.time()
        tab_nonhitting.append(((y - x)/10))
    total_tab.append(tab_nonhitting)

plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[0], label="0.01")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[1], label="0.1")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[2], label="1")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[3], label="2")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[4], label="5")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[5], label="10")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[6], label="20")
plt.ylabel('time in seconds')
plt.xlabel('number of nodes')
plt.legend()
plt.savefig('non_hitting.png')
plt.clf()

theta_tab = [0.01, 0.1, 1, 2, 5, 10]
print("-- Randomized short path with capacity constraint")
total_tab = []
for theta_val in theta_tab:
    print(theta_val)
    tab_capacity = []
    for i in range(len(list_of_dataset)):
        x = time.time()
        maxflow = 0
        for t in range(1):
            graph, maxflow = capacity_constraint(list_of_dataset[i].copy(), theta=theta_val)
        print(maxflow)
        y = time.time()
        tab_capacity.append(((y - x)/1))
    total_tab.append(tab_capacity)

plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[0], label="0.01")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[1], label="0.1")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[2], label="1")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[3], label="2")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[4], label="5")
plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[5], label="10")
plt.ylabel('time in seconds')
plt.xlabel('number of nodes')
plt.legend()
plt.savefig('rsp_capa.png')
