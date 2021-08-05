import networkx as nx
import matplotlib.pyplot as plt
#minimum cost flow algorithms
from algorithms.minimum_flow.cycle_canceling import *
from algorithms.minimum_flow.successive_shortest_path import *
from algorithms.minimum_flow.primal_dual import *
from algorithms.minimum_flow.out_of_kilter import *
from algorithms.minimum_flow.constrainedBoP_hitting import *
from algorithms.minimum_flow.constrainedBoP_nonhitting import *
from algorithms.minimum_flow.linear_programming import *
from algorithms.minimum_flow.linear_programming_cvx import *
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

#from ahuja book
#4 nodes
G2 = nx.DiGraph()
G2.add_edge(0, 1, weight=2, capacity=1000, flow=0)
G2.add_edge(0, 2, weight=2, capacity=1000, flow=0)
G2.add_edge(1, 2, weight=1, capacity=1000, flow=0)
G2.add_edge(1, 3, weight=3, capacity=1000, flow=0)
G2.add_edge(2, 3, weight=1, capacity=1000, flow=0)
G2.nodes[0]['b'] = 4
G2.nodes[3]['b'] = -4
list_of_dataset.append(G2)

#from ahuja book
#4 nodes
G3 = nx.DiGraph()
G3.add_edge(0, 2, weight=2, capacity=1000, flow=0)
G3.add_edge(0, 1, weight=2, capacity=1000, flow=0)
G3.add_edge(1, 2, weight=1, capacity=1000, flow=0)
G3.add_edge(1, 3, weight=3, capacity=1000, flow=0)
G3.add_edge(2, 3, weight=1, capacity=1000, flow=0)
G3.nodes[0]['b'] = 6
G3.nodes[3]['b'] = -6
list_of_dataset.append(G3)

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

####################################
# Run Minimum Cost Flow Algorithms #
####################################
print("")
print("--- Minimum Cost Flow Algorithms ---")
print("")
#Cycle-canceling Algorithm
print("-- Cycle-canceling")
for i in range(len(list_of_dataset)):
    graph, flow, cost = cycle_canceling(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
#Successive shortest path Algorithm
print("-- Successive shortest path")
for i in range(len(list_of_dataset)):
    graph, flow, cost = successive_shortest_path(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
#Primal Dual Algorithm
print("-- Primal dual")
for i in range(len(list_of_dataset)):
    graph, flow, cost = primal_dual(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
#Out Of Kilter Algorithm
print("-- Out-of-kilter")
for i in range(len(list_of_dataset)):
    graph, flow, cost = out_of_kilter(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
#Constrained hitting Bag-Of-Pathsµ
print("-- Constrained hitting bag-of-paths")
for i in range(len(list_of_dataset)):
    graph, flow, cost = constrainedBop_hitting(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
#Constrained non-hitting Bag-Of-Paths
print("-- Constrained non-hitting bag-of-paths")
for i in range(len(list_of_dataset)):
    graph, flow, cost = constrainedBop_nonhitting(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
#Linear programming
print("-- Linear programming with an optimize simplex method")
for i in range(len(list_of_dataset)):
    graph, flow, cost = linear_programming(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
#Linear programming
print("-- Linear programming with CVX")
for i in range(len(list_of_dataset)):
    graph, flow, cost = linear_programming_cvx(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
