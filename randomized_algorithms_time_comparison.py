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

#https://www.topcoder.com/thrive/articles/Minimum%20Cost%20Flow%20Part%20Two:%20Algorithms
#4 nodes
G = nx.DiGraph()
G.add_edge(0, 2, weight=1, capacity=1000, flow=0)
G.add_edge(0, 3, weight=2, capacity=1000, flow=0)
G.add_edge(1, 2, weight=1, capacity=1000, flow=0)
G.add_edge(1, 3, weight=2, capacity=1000, flow=0)
G.nodes[0]['b'] = 2
G.nodes[1]['b'] = 2
G.nodes[2]['b'] = -2
G.nodes[3]['b'] = -2
list_of_dataset.append(G)

#6 nodes
G4 = nx.DiGraph()
G4.add_edge(0, 1, weight=5, capacity=1000, flow=0)
G4.add_edge(0, 2, weight=6, capacity=1000, flow=0)
G4.add_edge(1, 2, weight=4, capacity=1000, flow=0)
G4.add_edge(1, 3, weight=12, capacity=1000, flow=0)
G4.add_edge(2, 4, weight=3, capacity=1000, flow=0)
G4.add_edge(3, 2, weight=8, capacity=1000, flow=0)
G4.add_edge(4, 3, weight=9, capacity=1000, flow=0)
G4.add_edge(3, 5, weight=5, capacity=1000, flow=0)
G4.add_edge(4, 5, weight=1, capacity=1000, flow=0)
G4.nodes[0]['b'] = 23
G4.nodes[5]['b'] = -23
list_of_dataset.append(G4)

#https://www.chegg.com/homework-help/questions-and-answers/formulate-graph-solve-minimum-cost-flow-problem-q7629379
#8 nodes
G5 = nx.DiGraph()
G5.add_edge(0, 1, weight=15, capacity=1000, flow=0)
G5.add_edge(0, 2, weight=10, capacity=1000, flow=0)
G5.add_edge(1, 3, weight=10, capacity=1000, flow=0)
G5.add_edge(1, 4, weight=10, capacity=1000, flow=0)
G5.add_edge(1, 5, weight=5, capacity=1000, flow=0)
G5.add_edge(1, 2, weight=5, capacity=1000, flow=0)
G5.add_edge(2, 4, weight=25, capacity=1000, flow=0)
G5.add_edge(2, 5, weight=8, capacity=1000, flow=0)
G5.add_edge(3, 4, weight=30, capacity=1000, flow=0)
G5.add_edge(3, 6, weight=30, capacity=1000, flow=0)
G5.add_edge(4, 6, weight=10, capacity=1000, flow=0)
G5.add_edge(4, 7, weight=10, capacity=1000, flow=0)
G5.add_edge(5, 6, weight=30, capacity=1000, flow=0)
G5.add_edge(5, 7, weight=15, capacity=1000, flow=0)
G5.add_edge(6, 7, weight=30, capacity=1000, flow=0)
G5.nodes[0]['b'] = 100
G5.nodes[6]['b'] = -25
G5.nodes[7]['b'] = -75
list_of_dataset.append(G5)

#22 nodes
G6 = nx.DiGraph()
G6.add_edge(0, 1, weight=2, capacity=1000, flow=0)
G6.add_edge(0, 2, weight=2, capacity=1000, flow=0)
G6.add_edge(0, 3, weight=2, capacity=1000, flow=0)
G6.add_edge(0, 4, weight=2, capacity=1000, flow=0)
G6.add_edge(1, 5, weight=1, capacity=1000, flow=0)
G6.add_edge(1, 6, weight=4, capacity=1000, flow=0)
G6.add_edge(2, 7, weight=1, capacity=1000, flow=0)
G6.add_edge(2, 8, weight=4, capacity=1000, flow=0)
G6.add_edge(3, 9, weight=8, capacity=1000, flow=0)
G6.add_edge(3, 10, weight=2, capacity=1000, flow=0)
G6.add_edge(4, 11, weight=1, capacity=1000, flow=0)
G6.add_edge(5, 12, weight=1, capacity=1000, flow=0)
G6.add_edge(6, 12, weight=4, capacity=1000, flow=0)
G6.add_edge(7, 13, weight=6, capacity=1000, flow=0)
G6.add_edge(8, 13, weight=7, capacity=1000, flow=0)
G6.add_edge(9, 14, weight=2, capacity=1000, flow=0)
G6.add_edge(10, 14, weight=9, capacity=1000, flow=0)
G6.add_edge(11, 15, weight=2, capacity=1000, flow=0)
G6.add_edge(12, 16, weight=2, capacity=1000, flow=0)
G6.add_edge(13, 16, weight=5, capacity=1000, flow=0)
G6.add_edge(13, 17, weight=1, capacity=1000, flow=0)
G6.add_edge(14, 17, weight=5, capacity=1000, flow=0)
G6.add_edge(14, 18, weight=1, capacity=1000, flow=0)
G6.add_edge(15, 18, weight=1, capacity=1000, flow=0)
G6.add_edge(16, 19, weight=1, capacity=1000, flow=0)
G6.add_edge(17, 19, weight=5, capacity=1000, flow=0)
G6.add_edge(17, 20, weight=6, capacity=1000, flow=0)
G6.add_edge(18, 20, weight=5, capacity=1000, flow=0)
G6.add_edge(19, 21, weight=5, capacity=1000, flow=0)
G6.add_edge(20, 21, weight=5, capacity=1000, flow=0)
G6.nodes[0]['b'] = 100
G6.nodes[21]['b'] = -100
list_of_dataset.append(G6)

#44 nodes
G7 = nx.DiGraph()
#add G6
for (i,j) in G6.edges():
    cost = G6[i][j]["weight"]
    G7.add_edge(i, j, weight=cost, capacity=1000, flow=0)
G7.add_edge(21, 22, weight=2, capacity=1000, flow=0)
G7.add_edge(21, 23, weight=2, capacity=1000, flow=0)
G7.add_edge(21, 24, weight=2, capacity=1000, flow=0)
G7.add_edge(21, 25, weight=2, capacity=1000, flow=0)
G7.add_edge(22, 26, weight=1, capacity=1000, flow=0)
G7.add_edge(22, 27, weight=4, capacity=1000, flow=0)
G7.add_edge(23, 28, weight=1, capacity=1000, flow=0)
G7.add_edge(23, 29, weight=4, capacity=1000, flow=0)
G7.add_edge(24, 30, weight=8, capacity=1000, flow=0)
G7.add_edge(24, 31, weight=2, capacity=1000, flow=0)
G7.add_edge(25, 32, weight=1, capacity=1000, flow=0)
G7.add_edge(26, 33, weight=1, capacity=1000, flow=0)
G7.add_edge(27, 33, weight=4, capacity=1000, flow=0)
G7.add_edge(28, 34, weight=6, capacity=1000, flow=0)
G7.add_edge(29, 34, weight=7, capacity=1000, flow=0)
G7.add_edge(30, 35, weight=2, capacity=1000, flow=0)
G7.add_edge(31, 35, weight=9, capacity=1000, flow=0)
G7.add_edge(32, 36, weight=2, capacity=1000, flow=0)
G7.add_edge(33, 37, weight=2, capacity=1000, flow=0)
G7.add_edge(34, 37, weight=5, capacity=1000, flow=0)
G7.add_edge(34, 38, weight=1, capacity=1000, flow=0)
G7.add_edge(35, 38, weight=5, capacity=1000, flow=0)
G7.add_edge(35, 39, weight=1, capacity=1000, flow=0)
G7.add_edge(36, 39, weight=1, capacity=1000, flow=0)
G7.add_edge(37, 40, weight=1, capacity=1000, flow=0)
G7.add_edge(38, 40, weight=5, capacity=1000, flow=0)
G7.add_edge(38, 41, weight=6, capacity=1000, flow=0)
G7.add_edge(39, 41, weight=5, capacity=1000, flow=0)
G7.add_edge(40, 42, weight=5, capacity=1000, flow=0)
G7.add_edge(41, 42, weight=5, capacity=1000, flow=0)
G7.nodes[0]['b'] = 100
G7.nodes[42]['b'] = -100
list_of_dataset.append(G7)

#generation of graph with 100 nodes
T = nx.gn_graph(100, seed=1)
G8 = nx.DiGraph()
for node_i,node_j in T.edges():
    G8.add_edge(node_j, node_i, weight=randrange(1,5), capacity=randrange(10,100), flow=0)
list_of_no_succesors = []
for node in G8.nodes():
    lenght = sum(1 for _ in G8.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G8.add_edge(node_no_succ, 100, weight=randrange(1,5), capacity=randrange(10,100), flow=0)
G8.nodes[0]['b'] = 100
G8.nodes[100]['b'] = -100
list_of_dataset.append(G8)

#generation of graph with 500 nodes
T = nx.gn_graph(500, seed=1)
G9 = nx.DiGraph()
for node_i,node_j in T.edges():
    G9.add_edge(node_j, node_i, weight=randrange(1,5), capacity=randrange(10,100), flow=0)
list_of_no_succesors = []
for node in G9.nodes():
    lenght = sum(1 for _ in G9.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G9.add_edge(node_no_succ, 500, weight=randrange(1,5), capacity=randrange(10,100), flow=0)
G9.nodes[0]['b'] = 100
G9.nodes[500]['b'] = -100
list_of_dataset.append(G9)

#generation of graph with 1000 nodes
T = nx.gn_graph(1000, seed=1)
G10 = nx.DiGraph()
for node_i,node_j in T.edges():
    G10.add_edge(node_j, node_i, weight=randrange(1,5), capacity=randrange(10,100), flow=0)
list_of_no_succesors = []
for node in G10.nodes():
    lenght = sum(1 for _ in G10.successors(node))
    if lenght==0:
        list_of_no_succesors.append(node)
for node_no_succ in list_of_no_succesors:
    G10.add_edge(node_no_succ, 1000, weight=randrange(1,5), capacity=randrange(10,100), flow=0)
G10.nodes[0]['b'] = 100
G10.nodes[1000]['b'] = -100
list_of_dataset.append(G10)

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
        for t in range(1):
            graph, flow, cost = constrainedBop_hitting(list_of_dataset[i].copy(), theta=theta_val)
        print(cost)
        y = time.time()
        tab_hitting.append(((y - x)/1))
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
        for t in range(1):
            graph, flow, cost = constrainedBop_nonhitting(list_of_dataset[i].copy(), theta=theta_val)
        print(cost)
        y = time.time()
        tab_nonhitting.append(((y - x)/1))
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
#plt.plot([4, 6, 8, 22, 44, 100, 500, 1000],total_tab[6], label="15")
plt.ylabel('time in seconds')
plt.xlabel('number of nodes')
plt.legend()
plt.savefig('rsp_capa.png')