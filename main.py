import networkx as nx
import matplotlib.pyplot as plt
#minimum cost flow algorithms
from algorithms.minimum_flow.cycle_canceling import *
from algorithms.minimum_flow.successive_shortest_path import *
from algorithms.minimum_flow.primal_dual import *
from algorithms.minimum_flow.out_of_kilter import *
from algorithms.minimum_flow.constrainedBoP_hitting import *
from algorithms.minimum_flow.constrainedBoP_nonhitting import *
#maximum flow algorithms
from algorithms.maximum_flow.generic_augmenting_path import *
from algorithms.maximum_flow.preflow_push import *
#graph functions
from algorithms.graph_functions.api import *

###########
# DATASET #
###########

list_of_dataset = []

G = nx.DiGraph()
G.add_edge(0, 1, weight=5, capacity=16, flow=0)
G.add_edge(0, 2, weight=6, capacity=13, flow=0)
G.add_edge(1, 2, weight=4, capacity=10, flow=0)
G.add_edge(1, 3, weight=12, capacity=12, flow=0)
G.add_edge(2, 4, weight=3, capacity=14, flow=0)
G.add_edge(3, 2, weight=8, capacity=9, flow=0)
G.add_edge(4, 3, weight=9, capacity=7, flow=0)
G.add_edge(3, 5, weight=5, capacity=20, flow=0)
G.add_edge(4, 5, weight=1, capacity=4, flow=0)
G.add_edge(5, 0, weight=0, capacity=4, flow=0)
G.nodes[0]['b'] = 23
G.nodes[5]['b'] = -23
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

#https://www.chegg.com/homework-help/questions-and-answers/formulate-graph-solve-minimum-cost-flow-problem-q7629379
G3 = nx.DiGraph()
G3.add_edge(0, 1, weight=15, capacity=75, flow=0)
G3.add_edge(0, 2, weight=10, capacity=50, flow=0)
G3.add_edge(1, 3, weight=10, capacity=30, flow=0)
G3.add_edge(1, 4, weight=10, capacity=50, flow=0)
G3.add_edge(1, 5, weight=5, capacity=30, flow=0)
G3.add_edge(1, 2, weight=5, capacity=40, flow=0)
G3.add_edge(2, 4, weight=25, capacity=40, flow=0)
G3.add_edge(2, 5, weight=8, capacity=60, flow=0)
G3.add_edge(3, 4, weight=30, capacity=60, flow=0)
G3.add_edge(3, 6, weight=30, capacity=100, flow=0)
G3.add_edge(4, 6, weight=10, capacity=40, flow=0)
G3.add_edge(4, 7, weight=10, capacity=40, flow=0)
G3.add_edge(5, 6, weight=30, capacity=50, flow=0)
G3.add_edge(5, 7, weight=15, capacity=80, flow=0)
G3.add_edge(6, 7, weight=30, capacity=100, flow=0)
G3.nodes[0]['b'] = 100
G3.nodes[6]['b'] = -25
G3.nodes[7]['b'] = -75
list_of_dataset.append(G3)

#https://www.topcoder.com/thrive/articles/Minimum%20Cost%20Flow%20Part%20Two:%20Algorithms
G4 = nx.DiGraph()
G4.add_edge(0, 1, weight=1, capacity=7, flow=0)
G4.add_edge(0, 2, weight=5, capacity=7, flow=0)
G4.add_edge(1, 2, weight=2, capacity=2, flow=0)
G4.add_edge(1, 3, weight=8, capacity=3, flow=0)
G4.add_edge(2, 3, weight=3, capacity=3, flow=0)
G4.add_edge(2, 4, weight=4, capacity=2, flow=0)
G4.add_edge(3, 0, weight=0, capacity=4, flow=0)
G4.add_edge(4, 0, weight=0, capacity=4, flow=0)
G4.nodes[0]['b'] = 5
G4.nodes[3]['b'] = -3
G4.nodes[4]['b'] = -2
list_of_dataset.append(G4)

#https://www.topcoder.com/thrive/articles/Minimum%20Cost%20Flow%20Part%20Two:%20Algorithms
G5 = nx.DiGraph()
G5.add_edge(0, 2, weight=1, capacity=1, flow=0)
G5.add_edge(0, 3, weight=2, capacity=1, flow=0)
G5.add_edge(1, 2, weight=1, capacity=1, flow=0)
G5.add_edge(1, 3, weight=2, capacity=2, flow=0)
G5.nodes[0]['b'] = 2
G5.nodes[1]['b'] = 2
G5.nodes[2]['b'] = -2
G5.nodes[3]['b'] = -2
list_of_dataset.append(G5)

#from ahuja book
G6 = nx.DiGraph()
G6.add_edge(0, 2, weight=2, capacity=4, flow=0)
G6.add_edge(0, 1, weight=2, capacity=2, flow=0)
G6.add_edge(1, 2, weight=1, capacity=3, flow=0)
G6.add_edge(1, 3, weight=3, capacity=1, flow=0)
G6.add_edge(2, 3, weight=1, capacity=5, flow=0)
G6.nodes[0]['b'] = 6
G6.nodes[3]['b'] = -6
list_of_dataset.append(G6)

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
#Constrained hitting Bag-Of-Paths
print("-- Constrained hitting bag-of-paths (with infinite capacity consider)")
for i in range(len(list_of_dataset)):
    graph, flow, cost = constrainedBop_hitting(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)
#Constrained non-hitting Bag-Of-Paths
print("-- Constrained non-hitting bag-of-paths (with infinite capacity consider)")
for i in range(len(list_of_dataset)):
    graph, flow, cost = constrainedBop_nonhitting(list_of_dataset[i].copy())
    print("Solution of dataset n°"+str(i+1)+" : Flow = "+str(flow)+" : Cost = "+str(cost))
    #print_graph(graph)

#constrainedBop_nonhitting(G4)
#bop_brut(G7)
#exit()
