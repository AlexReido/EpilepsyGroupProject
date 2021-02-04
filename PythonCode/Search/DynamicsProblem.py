from pymoo.model.problem import Problem
from PythonCode.Search.SimulateDynamics import fitness_function
import numpy as np


class DynamicsProblem(Problem):

    def __init__(self, n_decision_var, coupling_value, network, timesteps):
        super().__init__(n_var=n_decision_var,
                         n_obj=2,
                         n_constr=0)
        self.w = coupling_value
        self.net = network
        self.t = timesteps
        self.seed = 1337

    def _evaluate(self, X, out, *args, **kwargs):
        y = fitness_function(X, self.w, self.net, self.t)  # self.seed
        f1 = y[:, 0]
        f2 = y[:, 1]
        out["F"] = np.column_stack([f1, f2])

        # problem constraints
        # f1 should be greater than 0?
        # g1 = 2 * (X[:, 0] - 0.1) * (X[:, 0] - 0.9) / 0.18
        # g2 = - 20 * (X[:, 0] - 0.4) * (X[:, 0] - 0.6) / 4.8
        # out["G"] = np.column_stack([g1, g2])
