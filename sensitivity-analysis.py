from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

x = solver.NumVar(0.0, solver.infinity(), "x")
y = solver.NumVar(0.0, solver.infinity(), "y")

# Constraint 0: 4x + 10y <= 100
solver.Add(4*x + 10*y <= 100, "c0")

# Constraint 1: 2x + y <= 22
solver.Add(2*x + y <= 22, "c1")

# Constraint 2: 3x + 3y <= 39
solver.Add(3*x + 3*y <= 39, "c2")

# Objective: 60x + 50y
solver.Maximize(60*x + 50*y)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print('x =', x.solution_value())
    print('y =', y.solution_value())
else:
    print('The problem does not have an optimal solution.')

activities = solver.ComputeConstraintActivities()
o = [print({'Name': c.name(), 'shadow price': c.dual_value(), 'slack': c.ub() - activities[i]}) 
     for i, c in enumerate(solver.constraints())]
