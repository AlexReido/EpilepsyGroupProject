import numpy as np
from pymoo.algorithms.moead import MOEAD
from scipy import io
from SimulateDynamics import bni_find, fitness_function
from pymoo.model.problem import Problem

import CONSTANTS
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination, get_reference_directions
from pymoo.optimize import minimize


class MyProblem(Problem):

    def __init__(self, n_decision_var, coupling_value, network, timesteps):
        super().__init__(n_var=n_decision_var,
                         n_obj=2,
                         n_constr=0)
        self.w = coupling_value
        self.net = network
        self.t = timesteps
        self.seed = 1337

    def _evaluate(self, X, out, *args, **kwargs):
        y = fitness_function(X, self.w, self.net, self.t, self.seed)
        f1 = y[:, 0]
        f2 = y[:, 1]
        out["F"] = np.column_stack([f1, f2])

        # problem constraints
        # f1 should be greater than 0?
        #g1 = 2 * (X[:, 0] - 0.1) * (X[:, 0] - 0.9) / 0.18
        #g2 = - 20 * (X[:, 0] - 0.4) * (X[:, 0] - 0.6) / 4.8
        #out["G"] = np.column_stack([g1, g2])


def main(): # TODO is this needed? (has different timestep variable).
    network = io.loadmat('resources\\net.mat')
    net = network['net']

    # first check if the network has ones in its main diagonal (if yes we delete them)
    length_net = len(network)
    if (np.diag(network) == np.ones((length_net, 1))).all:
        network = network - np.eye(length_net)

    # compute the reference coupling value, for which BNI = 0.5
    ref_coupling, BNI_test_values, coupling_test_values = bni_find(net, t=40000)

    # apply the GA
    #for count_runs in range(CONSTANTS.num_GA_runs):
        # optimrun(CONSTANTS.num_gen, CONSTANTS.pop_size, count_runs, network, ref_coupling)


if __name__ == '__main__':
    network = io.loadmat('resources\\net.mat')  # TODO try with much smaller network to speed things up, or reduce N_N value?
    net = network['net']
    # compute the reference coupling value, for which BNI = 0.5
    TIMESTEPS = 40000
    ref_coupling, BNI_test_values, coupling_test_values = bni_find(net, TIMESTEPS)
    vectorized_problem = MyProblem(len(net), ref_coupling, net, TIMESTEPS)
    termination = get_termination("n_gen", 100)
    moeadalgo = MOEAD(
        get_reference_directions("energy", 2, 10),
        pop_size=10,
        sampling=get_sampling("bin_random"),
        crossover=get_crossover("bin_ux"),
        mutation=get_mutation("bin_bitflip"),
        eliminate_duplicates=True
    )

    nsgaalgo = NSGA2(
        pop_size=10,
        sampling=get_sampling("bin_random"),
        crossover=get_crossover("bin_ux"),
        mutation=get_mutation("bin_bitflip"),
        eliminate_duplicates=True
    )


    res = minimize(vectorized_problem,
                   nsgaalgo,
                   termination,
                   seed=1,
                   save_history=True,
                   verbose=True)
    print("NSGA-II")
    print("Number of Nodes, (1-Delta BNI value)")
    print(res.F)  # final fitness
    print("===================================")
    res = minimize(vectorized_problem,
                   moeadalgo,
                   termination,
                   seed=1,
                   save_history=True,
                   verbose=True)

    print("===================================")
    print("MOEAD")
    print("Number of Nodes, (1-Delta BNI value)")
    print(res.F)  # final fitness
