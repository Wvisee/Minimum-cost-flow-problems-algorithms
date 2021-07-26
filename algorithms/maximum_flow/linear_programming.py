from ortools.linear_solver import pywraplp
from ..graph_functions.api import *
import numpy as np

# Algorithms take from https://developers.google.com/optimization/lp/glop
def linear_programming(graph):
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver.CreateSolver('GLOP')

    source, sink = add_source_sink_maxflow_rsp_with_constraint(graph)
    graph.add_edge(sink, source, weight=0, capacity=sys.maxsize, flow=0)

    # Create the two variables and let them take on any non-negative value.
    n = len(graph)
    var = {}
    for i,j in graph.edges():
        capacity = graph[i][j]["capacity"]
        #print('x'+str(i)+str(j))
        var[(i,j)] = solver.NumVar(0, capacity, 'x'+str(i)+str(j))

    #print('Number of variables =', solver.NumVariables())

    #somme des flow in = flow out
    for node in graph.nodes():
        In = ""
        Out = ""
        for child in graph.neighbors(node):
            In = In + "var[("+str(node)+","+str(child)+")] "
        In = In.split(" ")[:-1]
        In = ' + '.join(In)
        for parent in graph.predecessors(node):
            Out = Out + "var[("+str(parent)+","+str(node)+")] "
        Out = Out.split(" ")[:-1]
        Out = ' + '.join(Out)
        expression = str(In) + " == " + str(Out)
        solver.Add(eval(expression))

    #max out et in
    solver.Maximize(eval("var[("+str(sink)+","+str(source)+")]"))

    # Solve the system.
    status = solver.Solve()

    for i,j in graph.edges():
        graph[i][j]["flow"] = eval("var[("+str(i)+","+str(j)+")]").solution_value()

    return graph,solver.Objective().Value()

    '''
    if status == pywraplp.Solver.OPTIMAL:
        print('Solution:')
        print('Objective value =', solver.Objective().Value())
        print('x =', x.solution_value())
        print('y =', y.solution_value())
    else:
        print('The problem does not have an optimal solution.')

    print('\nAdvanced usage:')
    print('Problem solved in %f milliseconds' % solver.wall_time())
    print('Problem solved in %d iterations' % solver.iterations())
    '''
