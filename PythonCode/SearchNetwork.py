import random

import numpy as np
from pymoo.algorithms.moead import MOEAD
from pymoo.model.crossover import Crossover
from pymoo.operators.crossover.util import crossover_mask
from pymoo.operators.sampling.random_sampling import BinaryRandomSampling
from pymoo.operators.mutation.bitflip_mutation import BinaryBitflipMutation
from pymoo.operators.crossover.uniform_crossover import UniformCrossover
from scipy import io
from SimulateDynamics import bni_find, fitness_function
from pymoo.model.problem import Problem

import CONSTANTS
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation, get_termination, get_reference_directions, \
    get_visualization
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


class BinaryRandomSamplingLimit(BinaryRandomSampling):
    def __init__(self, maxNodes) -> None:
        self.maxNodes = maxNodes
        super().__init__()

    def _do(self, problem, n_samples, **kwargs):
        # val = np.random.random((n_samples, problem.n_var))
        # x = (val < 0.5).astype(np.bool)
        # print(x)
        # print(x.shape)
        # return x
        # print("sampling")
        pop = []

        for i in range(n_samples):
            number_resected = random.randrange(0, self.maxNodes)
            indexes = random.sample(range(problem.n_var), number_resected)
            nodes = [False] * problem.n_var
            nodes = [True if i in indexes else x for i, x in enumerate(nodes)]
            # print(nodes)
            pop.append(nodes)
        # print(pop)
        return pop


class UniformCrossoverLimit(Crossover):
    def __init__(self, max_nodes, **kwargs):
        self.max_nodes = max_nodes
        super().__init__(2, 2, **kwargs)

    def _do(self, problem, X, **kwargs):
        """

        :param problem:
        :param X:  X is structured such that it is a list of 2 (_ == 2) sublists
        These sublists are the sets of parents (there are n_matings parents in each)
        eg for a population of ten the shape is 2 5 59 such that there are two sets
        of ten five parents each with 59 values.
        n_var is the number of nodes (len of network)
        :param kwargs:
        :return:
        """
        # print("Crossover")
        within_limit = False
        _, n_matings, n_var = X.shape
        # print(X.shape)
        # print(X)
        i = 0
        while (within_limit == False):
            within_limit = True
            M = np.random.random((n_matings, n_var)) < 0.5

            _X = crossover_mask(X, M)
            for eachside in _X:
                for eachchild in eachside:
                    # print(sum(eachchild))
                    # print(eachchild)

                    if (sum(eachchild) > self.max_nodes):
                        within_limit = False
            i += 1
            if i > 20:
                raise RuntimeError("Stuck reducing the number of nodes during crossover")
        # print(_X)
        return _X


from pymoo.model.mutation import Mutation


class BinaryBitflipMutationLimit(Mutation):

    def __init__(self, max_nodes, prob=None):
        self.max_nodes = max_nodes
        super().__init__()
        self.prob = prob

    def _do(self, problem, X, **kwargs):
        # print("mutating")
        if self.prob is None:
            self.prob = 1.0 / problem.n_var
        # print(X.shape)
        # print(X)
        # print("Probability = ", str(self.prob))
        X = X.astype(np.bool)
        _X = []
        for nodelist in X:
            inlimit = False
            while not inlimit:
                newnodelist = np.full(nodelist.shape, np.inf)

                M = np.random.random(nodelist.shape)
                flip, no_flip = M < self.prob, M >= self.prob

                newnodelist[flip] = np.logical_not(nodelist[flip])
                newnodelist[no_flip] = nodelist[no_flip]
                if sum(newnodelist) <= self.max_nodes:
                    inlimit = True
                    _X.append(list(newnodelist.astype(np.bool)))
        # print(_X)
        return _X  # .astype(np.bool)


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

    def search(self, nGen=100, max_nodes=20):
        # compute the reference coupling value, for which BNI = 0.5
        print("Finding reference coupling:")
        ref_coupling, BNI_test_values, coupling_test_values = bni_find(self.net, self.timesteps)
        vectorized_problem = MyProblem(len(self.net), ref_coupling, self.net, self.timesteps)
        termination = get_termination("n_gen", nGen)

        # sampling = get_sampling("bin_random"),
        # crossover = get_crossover("bin_ux"),
        # mutation = get_mutation("bin_bitflip"),
        if self.searchAlgo == "MOEAD":
            print("MOEAD")
            search = MOEAD(

                get_reference_directions("das-dennis", 2, n_partitions=10),
                # pop_size=8,
                n_neighbors=8,
                # sampling = get_sampling("bin_random"),
                # crossover = get_crossover("bin_ux"),
                # mutation = get_mutation("bin_bitflip"),
                sampling=BinaryRandomSamplingLimit(max_nodes),
                crossover=UniformCrossoverLimit(max_nodes),
                mutation=BinaryBitflipMutationLimit(max_nodes),
                eliminate_duplicates=True
            )
        elif self.searchAlgo == "NSGA2":
            print("NSGA-II")
            search = NSGA2(
                pop_size=10,
                sampling=BinaryRandomSamplingLimit(max_nodes),
                crossover=UniformCrossoverLimit(max_nodes),
                mutation=BinaryBitflipMutationLimit(max_nodes),
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
    # ref_dirs = get_reference_directions("das-dennis", 2, n_partitions=8)
    #
    # get_visualization("scatter").add(ref_dirs).show()
    sn = SearchNetwork("NSGA2")
    res = sn.search(30, 15)
    print("Nodes")
    for nlist in res.X:
        node_indexes = [i for i, x in enumerate(nlist) if x]
        print(node_indexes)
