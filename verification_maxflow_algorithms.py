import networkx as nx
import matplotlib.pyplot as plt
#maximum flow algorithms
from algorithms.maximum_flow.generic_augmenting_path import *
from algorithms.maximum_flow.preflow_push import *
from algorithms.maximum_flow.capacity_constraint import *
from algorithms.maximum_flow.linear_programming import *
#graph functions
from algorithms.graph_functions.api import *

###########
# DATASET #
###########

list_of_dataset = []

#https://www.topcoder.com/thrive/articles/Minimum%20Cost%20Flow%20Part%20Two:%20Algorithms
G = nx.DiGraph()
G.add_edge(0, 2, weight=1, capacity=1, flow=0)
G.add_edge(0, 3, weight=2, capacity=1, flow=0)
G.add_edge(1, 2, weight=1, capacity=1, flow=0)
G.add_edge(1, 3, weight=2, capacity=2, flow=0)
G.nodes[0]['b'] = 2
G.nodes[1]['b'] = 2
G.nodes[2]['b'] = -2
G.nodes[3]['b'] = -2
list_of_dataset.append(G)

#from ahuja book
G2 = nx.DiGraph()
G2.add_edge(0, 1, weight=2, capacity=4, flow=0)
G2.add_edge(0, 2, weight=2, capacity=2, flow=0)
G2.add_edge(1, 2, weight=1, capacity=2, flow=0)
G2.add_edge(1, 3, weight=3, capacity=3, flow=0)
G2.add_edge(2, 3, weight=1, capacity=5, flow=0)
G2.nodes[0]['b'] = 4
G2.nodes[3]['b'] = -4
list_of_dataset.append(G2)

#from ahuja book
G3 = nx.DiGraph()
G3.add_edge(0, 2, weight=2, capacity=4, flow=0)
G3.add_edge(0, 1, weight=2, capacity=2, flow=0)
G3.add_edge(1, 2, weight=1, capacity=3, flow=0)
G3.add_edge(1, 3, weight=3, capacity=1, flow=0)
G3.add_edge(2, 3, weight=1, capacity=5, flow=0)
G3.nodes[0]['b'] = 6
G3.nodes[3]['b'] = -6
list_of_dataset.append(G3)

G4 = nx.DiGraph()
G4.add_edge(0, 1, weight=5, capacity=16, flow=0)
G4.add_edge(0, 2, weight=6, capacity=13, flow=0)
G4.add_edge(1, 2, weight=4, capacity=10, flow=0)
G4.add_edge(1, 3, weight=12, capacity=12, flow=0)
G4.add_edge(2, 4, weight=3, capacity=14, flow=0)
G4.add_edge(3, 2, weight=8, capacity=9, flow=0)
G4.add_edge(4, 3, weight=9, capacity=7, flow=0)
G4.add_edge(3, 5, weight=5, capacity=19, flow=0)
G4.add_edge(4, 5, weight=1, capacity=4, flow=0)
G4.nodes[0]['b'] = 23
G4.nodes[5]['b'] = -23
list_of_dataset.append(G4)

#https://www.chegg.com/homework-help/questions-and-answers/formulate-graph-solve-minimum-cost-flow-problem-q7629379
G5 = nx.DiGraph()
G5.add_edge(0, 1, weight=15, capacity=75, flow=0)
G5.add_edge(0, 2, weight=10, capacity=50, flow=0)
G5.add_edge(1, 3, weight=10, capacity=30, flow=0)
G5.add_edge(1, 4, weight=10, capacity=50, flow=0)
G5.add_edge(1, 5, weight=5, capacity=30, flow=0)
G5.add_edge(1, 2, weight=5, capacity=40, flow=0)
G5.add_edge(2, 4, weight=25, capacity=40, flow=0)
G5.add_edge(2, 5, weight=8, capacity=60, flow=0)
G5.add_edge(3, 4, weight=30, capacity=60, flow=0)
G5.add_edge(3, 6, weight=30, capacity=100, flow=0)
G5.add_edge(4, 6, weight=10, capacity=40, flow=0)
G5.add_edge(4, 7, weight=10, capacity=40, flow=0)
G5.add_edge(5, 6, weight=30, capacity=50, flow=0)
G5.add_edge(5, 7, weight=15, capacity=80, flow=0)
G5.add_edge(6, 7, weight=30, capacity=100, flow=0)
G5.nodes[0]['b'] = 100
G5.nodes[6]['b'] = -25
G5.nodes[7]['b'] = -75
list_of_dataset.append(G5)

#22 nodes
G6 = nx.DiGraph()
G6.add_edge(0, 1, weight=25, capacity=1000, flow=0)
G6.add_edge(0, 2, weight=25, capacity=500, flow=0)
G6.add_edge(0, 3, weight=25, capacity=500, flow=0)
G6.add_edge(0, 4, weight=25, capacity=1000, flow=0)
G6.add_edge(1, 5, weight=18, capacity=500, flow=0)
G6.add_edge(1, 6, weight=42, capacity=1000, flow=0)
G6.add_edge(2, 7, weight=19, capacity=500, flow=0)
G6.add_edge(2, 8, weight=4, capacity=1000, flow=0)
G6.add_edge(3, 9, weight=80, capacity=500, flow=0)
G6.add_edge(3, 10, weight=32, capacity=1000, flow=0)
G6.add_edge(4, 11, weight=10, capacity=500, flow=0)
G6.add_edge(5, 12, weight=12, capacity=1000, flow=0)
G6.add_edge(6, 12, weight=40, capacity=500, flow=0)
G6.add_edge(7, 13, weight=60, capacity=1000, flow=0)
G6.add_edge(8, 13, weight=70, capacity=500, flow=0)
G6.add_edge(9, 14, weight=22, capacity=1000, flow=0)
G6.add_edge(10, 14, weight=99, capacity=1000, flow=0)
G6.add_edge(11, 15, weight=20, capacity=500, flow=0)
G6.add_edge(12, 16, weight=20, capacity=1000, flow=0)
G6.add_edge(13, 16, weight=50, capacity=1000, flow=0)
G6.add_edge(13, 17, weight=12, capacity=500, flow=0)
G6.add_edge(14, 17, weight=50, capacity=1000, flow=0)
G6.add_edge(14, 18, weight=12, capacity=1000, flow=0)
G6.add_edge(15, 18, weight=16, capacity=500, flow=0)
G6.add_edge(16, 19, weight=18, capacity=1000, flow=0)
G6.add_edge(17, 19, weight=50, capacity=500, flow=0)
G6.add_edge(17, 20, weight=60, capacity=1000, flow=0)
G6.add_edge(18, 20, weight=50, capacity=500, flow=0)
G6.add_edge(19, 21, weight=50, capacity=500, flow=0)
G6.add_edge(20, 21, weight=50, capacity=1000, flow=0)
G6.nodes[0]['b'] = 1500
G6.nodes[21]['b'] = -1500
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
G7.nodes[0]['b'] = 1500
G7.nodes[42]['b'] = -1500
list_of_dataset.append(G7)

###############################
# Run Maximum Flow Algorithms #
###############################
print("--- Maximum Flow Algorithms ---")
print("")
#generic augmenting path
print("-- Generic augmenting path")
for i in range(len(list_of_dataset)):
    graph, maxflow = generic_augmenting_path(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Maxflow = "+str(maxflow))
    #print_graph(graph)
#preflow push
print("-- Preflow push (FIFO implementation)")
for i in range(len(list_of_dataset)):
    graph, maxflow = preflow_push(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Maxflow = "+str(maxflow))
    #print_graph(graph)
#Linear programming with an optimize simplex method
print("-- Linear programming with an optimize simplex method")
for i in range(len(list_of_dataset)):
    graph, maxflow = linear_programming(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Maxflow = "+str(maxflow))
    #print_graph(graph)
#Randomized short path with capacity constraint
print("-- Randomized short path with capacity constraint")
for i in range(len(list_of_dataset)):
    graph, maxflow = capacity_constraint(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Maxflow = "+str(maxflow))
    #print_graph(graph)
