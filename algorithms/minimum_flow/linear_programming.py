from ortools.linear_solver import pywraplp
from ..graph_functions.api import *
import numpy as np

# Algorithms take from https://developers.google.com/optimization/lp/glop
def linear_programming(graph):
    """Linear programming sample."""
    # Instantiate a Glop solver, naming it LinearExample.
    solver = pywraplp.Solver.CreateSolver('GLOP')

    #b(i) vector representing the supply/demand
    n = len(graph)
    b = [0] * n
    for node in graph.nodes():
        if 'b' in graph.nodes[node]:
            i = graph.nodes[node]['b']
            if i < 0:
                b[node] = i
            elif i > 0:
                b[node] = i

    # Variable declaration. As capacity don't interest us in the work, we won't put them to the constraints
    var = {}
    for i,j in graph.edges():
        var[(i,j)] = solver.NumVar(0, solver.infinity(), 'x'+str(i)+str(j))

    #print('Number of variables =', solver.NumVariables())

    #somme flow out - somme des flow in = b(i)
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

        if Out=="":
            expression = "("+str(In)+")"+" == " + str(b[node])
            #print(expression)
            solver.Add(eval(expression))
        elif In=="":
            expression = " - "+"("+str(Out)+") == " + str(b[node])
            #print(expression)
            solver.Add(eval(expression))
        else:
            expression = "("+str(In)+")"+" - "+"("+str(Out)+") == " + str(b[node])
            #print(expression)
            solver.Add(eval(expression))

    #min sum of cost * flow
    exp = ""
    for i,j in graph.edges():
        cost = graph[i][j]["weight"]
        exp = exp + str(cost)+"*"+"var[("+str(i)+","+str(j)+")] "
    exp = exp.split(" ")[:-1]
    exp = ' + '.join(exp)

    solver.Minimize(eval(exp))

    # Solve the system.
    status = solver.Solve()

    for i,j in graph.edges():
        graph[i][j]["flow"] = eval("var[("+str(i)+","+str(j)+")]").solution_value()

    cost = compute_total_cost(graph)

    flow = 0
    for i in b:
        if i>0:
            flow = flow + i

    return graph,flow,cost

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
