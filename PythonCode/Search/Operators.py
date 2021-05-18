import random
import numpy as np

from pymoo.operators.sampling.random_sampling import BinaryRandomSampling
from pymoo.model.crossover import Crossover
from pymoo.operators.crossover.util import crossover_mask
from pymoo.model.mutation import Mutation
from pymoo.model.callback import Callback

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
            number_resected = random.randrange(1, self.maxNodes)
            indexes = random.sample(range(1, problem.n_var), number_resected)
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
                if sum(newnodelist) <= self.max_nodes and sum(newnodelist) != 0:
                    inlimit = True
                    _X.append(list(newnodelist.astype(np.bool)))
        # print(_X)
        return _X  # .astype(np.bool)


class MyCallback(Callback):

    def __init__(self, swp) -> None:
        super().__init__()
        self.n_evals = []
        self.opt = []
        self.swp=swp

    def notify(self, algorithm):

        self.n_evals.append(algorithm.evaluator.n_eval)
        # print(len(self.n_evals))
        results = []
        for ind in algorithm.opt:
            results.append(ind.F)

         # newline
        if self.swp != None:
        #     self.swp.nextgeneration()
            print("generation: ", algorithm.evaluator.n_eval)
            l = [list(l) for l in results]
            print("results: ", l)
            self.swp.result = {algorithm.evaluator.n_eval/10: l}

        self.opt.append(results)