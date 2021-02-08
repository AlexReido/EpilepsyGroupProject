import numpy as np
from pymoo.algorithms.moead import MOEAD
from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_termination, get_reference_directions
from pymoo.optimize import minimize
from scipy import io
from PythonCode.Search.SimulateDynamics import bni_find
from PythonCode.Search.DynamicsProblem import DynamicsProblem
from PythonCode.Search.Operators import *

def main():  # TODO is this needed? (has different timestep variable).
    network = io.loadmat('../resources/net.mat')
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
            network = io.loadmat('../resources/net.mat')
            self.net = network['net']
        else:
            self.net = network

    def search(self, nGen=100, max_nodes=20):
        # compute the reference coupling value, for which BNI = 0.5
        print("Finding reference coupling:")
        ref_coupling, BNI_test_values, coupling_test_values = bni_find(self.net, self.timesteps)
        vectorized_problem = DynamicsProblem(len(self.net), ref_coupling, self.net, self.timesteps)
        termination = get_termination("n_gen", nGen)
        callback = MyCallback()
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
                       callback=callback,
                       seed=1,
                       save_history=True,
                       verbose=True)

        print("Number of Nodes, (1-Delta BNI value)")
        print(res.F)  # final fitness
        return callback


if __name__ == '__main__':
    # ref_dirs = get_reference_directions("das-dennis", 2, n_partitions=8)
    #
    # get_visualization("scatter").add(ref_dirs).show()
    # TODO print time
    sn = SearchNetwork("NSGA2", timesteps=4000000)
    res = sn.search(30, 15)
    for i, generation in enumerate(res.opt):
        print("Generation: ", str(i))
        for ind in generation:
            print(ind[0], ind[1])
    # TODO print time
    # print("Nodes")
    # for nlist in res.X:
    #     node_indexes = [i for i, x in enumerate(nlist) if x]
    #     print(node_indexes)
