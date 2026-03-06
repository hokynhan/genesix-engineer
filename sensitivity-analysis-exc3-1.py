from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

x1 = solver.IntVar(0.0, solver.infinity(), "x1")  # Amount VEG1 to buy (in tons)
x2 = solver.IntVar(0.0, solver.infinity(), "x2")  # Amount VEG2 to buy
x3 = solver.IntVar(0.0, solver.infinity(), "x3")  # ... OIL1 ...
x4 = solver.IntVar(0.0, solver.infinity(),"x4")  # ... OIL2 ...
x5 = solver.IntVar(0.0, solver.infinity(), "x5")  # ... OIL2 ...
P = solver.IntVar(0.0, solver.infinity(), "P") # amount number of final product in tons

# ConstraNum limit: x1 + x2 <= 200
solver.Add(x1 + x2 <= 200, "c0")
# ConstraNum limit: x3 + x4 + x5 <= 250
solver.Add(x3 + x4 + x5 <= 250, "c1")
# hardness constrain 3<= ... <= 6
solver.Add(8.8*x1 + 6.1*x2 + 2*x3 + 4.2*x4 + 5*x5 - 3*P >= 0, "c2")
solver.Add(8.8*x1 + 6.1*x2 + 2*x3 + 4.2*x4 + 5*x5 - 6*P <= 0, "c3")
# Contrain equal mass
solver.Add( x1 + x2 + x3 + x4 + x5 - P == 0, "c4")
# Constrain positive
solver.Add(x1 >= 0, "c5")
solver.Add(x2 >= 0, "c6")
solver.Add(x3 >= 0, "c7")
solver.Add(x4 >= 0, "c8")
solver.Add(x5 >= 0, "c9")
solver.Add(P >= 0, "c10")

# Objective: maximize PROFIT
solver.Maximize(150*P - (110*x1 + 120*x2 + 130*x3 + 110*x4 + 115*x5))

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    print("Solution:")
    print("Objective value =", solver.Objective().Value())
    print("x1 =", x1.solution_value())
    print("x2 =", x2.solution_value())
    print("x3 =", x3.solution_value())
    print("x4 =", x4.solution_value())
    print("x5 =", x5.solution_value())
    print("P =", P.solution_value())
else:
    print("The problem does not have an optimal solution.")
