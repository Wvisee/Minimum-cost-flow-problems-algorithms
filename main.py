import networkx as nx
import matplotlib.pyplot as plt
from algorithms.Cycle_canceling import *
from algorithms.successive_shortest_path_top_coder import *

#dataset

G = nx.DiGraph()
G.add_edge(0, 1, weight=5, capacity=16, flow=0)
G.add_edge(0, 2, weight=6, capacity=13, flow=0)
G.add_edge(1, 2, weight=4, capacity=10, flow=0)
G.add_edge(2, 1, weight=2, capacity=4, flow=0)
G.add_edge(1, 3, weight=12, capacity=12, flow=0)
G.add_edge(2, 4, weight=3, capacity=14, flow=0)
G.add_edge(3, 2, weight=8, capacity=9, flow=0)
G.add_edge(4, 3, weight=9, capacity=7, flow=0)
G.add_edge(3, 5, weight=5, capacity=20, flow=0)
G.add_edge(4, 5, weight=1, capacity=4, flow=0)
#for successive_shortest_path
G.nodes[0]['b'] = 23
G.nodes[5]['b'] = -23

G2 = nx.DiGraph()
G2.add_edge(0, 1, weight=2, capacity=4, flow=0)
G2.add_edge(0, 2, weight=2, capacity=2, flow=0)
G2.add_edge(1, 2, weight=1, capacity=2, flow=0)
G2.add_edge(1, 3, weight=3, capacity=3, flow=0)
G2.add_edge(2, 3, weight=1, capacity=5, flow=0)
#for successive_shortest_path
G2.nodes[0]['b'] = 4
G2.nodes[3]['b'] = -4

#taken from
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
G3.add_edge(3, 6, weight=45, capacity=100, flow=0)
G3.add_edge(4, 6, weight=10, capacity=40, flow=0)
G3.add_edge(4, 7, weight=10, capacity=40, flow=0)
G3.add_edge(5, 6, weight=30, capacity=50, flow=0)
G3.add_edge(5, 7, weight=15, capacity=80, flow=0)
G3.add_edge(6, 7, weight=45, capacity=100, flow=0)
#abstract sink that connect the 2 real sink
G3.nodes[0]['b'] = 100
G3.nodes[6]['b'] = -25
G3.nodes[7]['b'] = -75

G4 = nx.DiGraph()
G4.add_edge(0, 1, weight=1, capacity=7, flow=0)
G4.add_edge(0, 2, weight=5, capacity=7, flow=0)
G4.add_edge(1, 2, weight=-2, capacity=2, flow=0)
G4.add_edge(1, 3, weight=8, capacity=3, flow=0)
G4.add_edge(2, 3, weight=-3, capacity=3, flow=0)
G4.add_edge(2, 4, weight=4, capacity=2, flow=0)
G4.nodes[0]['b'] = 5
G4.nodes[3]['b'] = -3
G4.nodes[4]['b'] = -2

#Cycle-canceling Algorithm
cycle_canceling(G.copy())
cycle_canceling(G2.copy())
cycle_canceling(G3.copy())
cycle_canceling(G4.copy())
#Successive shortest path Algorithm
successive_shortest_path(G.copy())
successive_shortest_path(G2.copy())
successive_shortest_path(G3.copy())
successive_shortest_path(G4.copy())
