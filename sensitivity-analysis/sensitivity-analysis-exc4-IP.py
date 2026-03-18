from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('CLP')

# # Decision variables (LP relaxation: 0 <= xi <= 1, continuous)
# x1 = solver.NumVar(0.0, 1.0, "x1")  # build factory in LA
# x2 = solver.NumVar(0.0, 1.0, "x2")  # build factory in SF
# x3 = solver.NumVar(0.0, 1.0, "x3")  # build warehouse in LA
# x4 = solver.NumVar(0.0, 1.0, "x4")  # build warehouse in SF

# Decision variables (0/1)
x1 = solver.IntVar(0, 1, "x1")  # build factory in LA
x2 = solver.IntVar(0, 1, "x2")  # build factory in SF
x3 = solver.IntVar(0, 1, "x3")  # build warehouse in LA
x4 = solver.IntVar(0, 1, "x4")  # build warehouse in SF

# Constraint Capital limit: 6x1 + 3x2 + 5x3 + 2x4 <= 10
solver.Add(6*x1 + 3*x2 + 5*x3 + 2*x4 <= 10, "c0")

# Constraint At most one warehouse: x3 + x4 <= 1
solver.Add(x3 + x4 <= 1, "c1")

# Constraint Warehouse only where a factory is built:
# x3 <= x1, x4 <= x2
solver.Add(x3 <= x1, "c2")
solver.Add(x4 <= x2, "c3")


# Objective: maximize Net Present Value ($M)
solver.Maximize(9*x1 + 5*x2 + 6*x3 + 4*x4)


status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Solution:")
    print("Objective value =", solver.Objective().Value())
    print("x1 =", x1.solution_value())
    print("x2 =", x2.solution_value())
    print("x3 =", x3.solution_value())
    print("x4 =", x4.solution_value())

    cap_used = (
        6*x1.solution_value()
        + 3*x2.solution_value()
        + 5*x3.solution_value()
        + 2*x4.solution_value()
    )
    print("Capital used =", cap_used, "/ 10")
else:
    print("The problem does not have an optimal solution.")
