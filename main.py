import networkx as nx
import matplotlib.pyplot as plt
from algorithms.Cycle_canceling import *

#dataset

G = nx.DiGraph() #best 23
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

G2 = nx.DiGraph() #best 6
G2.add_edge(0, 1, weight=2, capacity=4, flow=0)
G2.add_edge(0, 2, weight=2, capacity=2, flow=0)
G2.add_edge(1, 2, weight=1, capacity=2, flow=0)
G2.add_edge(1, 3, weight=3, capacity=3, flow=0)
G2.add_edge(2, 3, weight=1, capacity=5, flow=0)

#taken from
#https://www.chegg.com/homework-help/questions-and-answers/formulate-graph-solve-minimum-cost-flow-problem-q7629379
G3 = nx.DiGraph()
G3.add_edge(1, 2, weight=15, capacity=75, flow=0)
G3.add_edge(1, 3, weight=10, capacity=50, flow=0)
G3.add_edge(2, 4, weight=10, capacity=30, flow=0)
G3.add_edge(2, 5, weight=10, capacity=50, flow=0)
G3.add_edge(2, 6, weight=5, capacity=30, flow=0)
G3.add_edge(2, 3, weight=5, capacity=40, flow=0)
G3.add_edge(3, 5, weight=25, capacity=40, flow=0)
G3.add_edge(3, 6, weight=8, capacity=60, flow=0)
G3.add_edge(4, 5, weight=30, capacity=60, flow=0)
G3.add_edge(4, 7, weight=45, capacity=100, flow=0)
G3.add_edge(5, 7, weight=10, capacity=40, flow=0)
G3.add_edge(5, 8, weight=10, capacity=40, flow=0)
G3.add_edge(6, 7, weight=30, capacity=50, flow=0)
G3.add_edge(6, 8, weight=15, capacity=80, flow=0)
G3.add_edge(7, 8, weight=45, capacity=100, flow=0)
#abstract sink that connect the 2 real sink
G3.add_edge(7, 0, weight=0, capacity=25, flow=0)
G3.add_edge(8, 0, weight=0, capacity=75, flow=0)

#Cycle-canceling Algorithm
#cycle_canceling(G, 0, 5)
#cycle_canceling(G2, 0, 3)
cycle_canceling(G3, 1, 0)
