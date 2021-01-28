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
        y = fitness_function(X, self.w, self.net, self.t)  # self.seed
        f1 = y[:, 0]
        f2 = y[:, 1]
        out["F"] = np.column_stack([f1, f2])

        # problem constraints
        # f1 should be greater than 0?
        # g1 = 2 * (X[:, 0] - 0.1) * (X[:, 0] - 0.9) / 0.18
        # g2 = - 20 * (X[:, 0] - 0.4) * (X[:, 0] - 0.6) / 4.8
        # out["G"] = np.column_stack([g1, g2])


def main():  # TODO is this needed? (has different timestep variable).
    network = io.loadmat('resources\\net.mat')
    net = network['net']

    # first check if the network has ones in its main diagonal (if yes we delete them)
    length_net = len(network)
    if (np.diag(network) == np.ones((length_net, 1))).all:
        network = network - np.eye(length_net)

    # compute the reference coupling value, for which BNI = 0.5
    ref_coupling, BNI_test_values, coupling_test_values = bni_find(net, t=4000)

    # apply the GA
    # for count_runs in range(CONSTANTS.num_GA_runs):
    # optimrun(CONSTANTS.num_gen, CONSTANTS.pop_size, count_runs, network, ref_coupling)


class SearchNetwork:
    """
     binary random sampling, binary tournament selection, binary bit flip, and single point binary cross over
    """
    def __init__(self, searchAlgo, network=None, timesteps=4000):
        self.searchAlgo = searchAlgo
        self.timesteps = timesteps
        if network is None:
            network = io.loadmat('resources\\net.mat')
            self.net = network['net']
        else:
            self.net = network

    def search(self, nGen = 100):
        # compute the reference coupling value, for which BNI = 0.5
        print("Finding reference coupling:")
        ref_coupling, BNI_test_values, coupling_test_values = bni_find(self.net, self.timesteps)
        vectorized_problem = MyProblem(len(self.net), ref_coupling, self.net, self.timesteps)
        termination = get_termination("n_gen", nGen)

        if self.searchAlgo == "MOEAD":
            print("MOEAD")
            search = MOEAD(
                get_reference_directions("energy", 2, 10),
                pop_size=10,
                sampling=get_sampling("bin_random"),
                crossover=get_crossover("bin_ux"),
                mutation=get_mutation("bin_bitflip"),
                eliminate_duplicates=True
            )
        elif self.searchAlgo == "NSGA2":
            print("NSGA-II")
            search = NSGA2(
                pop_size=10,
                sampling=get_sampling("bin_random"),
                crossover=get_crossover("bin_ux"),
                mutation=get_mutation("bin_bitflip"),
                eliminate_duplicates=True
            )
        else:
            raise "Search algorithm " + self.searchAlgo + " not implemented"

        res = minimize(vectorized_problem,
                       search,
                       termination,
                       seed=1,
                       save_history=True,
                       verbose=True)

        print("Number of Nodes, (1-Delta BNI value)")
        print(res.F)  # final fitness
        return res


if __name__ == '__main__':

    sn = SearchNetwork("NSGA2")
    sn.search()
