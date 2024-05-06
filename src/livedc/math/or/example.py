#  ___________________________________________________________________________
#
#  Pyomo: Python Optimization Modeling Objects
#  Copyright (c) 2008-2024
#  National Technology and Engineering Solutions of Sandia, LLC
#  Under the terms of Contract DE-NA0003525 with National Technology and
#  Engineering Solutions of Sandia, LLC, the U.S. Government retains certain
#  rights in this software.
#  This software is distributed under the 3-clause BSD License.
#  ___________________________________________________________________________

# iterative1.py
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
from pprint import pprint
# https://pypi.org/project/cplex/
# https://pyomo.readthedocs.io/en/stable/working_models.html#changing-the-model-or-data-and-re-solving

# Create a solver
opt = pyo.SolverFactory('cplex',solver_io="python",validate=False,tee =False)
pprint (opt.__dict__)
#
# A simple model with binary variables and
# an empty constraint list.
#
model = pyo.AbstractModel()
model.n = pyo.Param(default=4)
model.x = pyo.Var(pyo.RangeSet(model.n), within=pyo.Binary)


def o_rule(model):
    return pyo.summation(model.x)


model.o = pyo.Objective(rule=o_rule)
model.c = pyo.ConstraintList()

# Create a model instance and optimize
instance = model.create_instance()
results = opt.solve(instance)
instance.display()

# Iterate to eliminate the previously found solution
for i in range(5):
    expr = 0
    for j in instance.x:
        if pyo.value(instance.x[j]) == 0:
            expr += instance.x[j]
        else:
            expr += 1 - instance.x[j]
    instance.c.add(expr >= 1)
    results = opt.solve(instance)
    print("\n===== iteration", i)
    instance.display()