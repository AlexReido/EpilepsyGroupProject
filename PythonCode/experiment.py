from scipy import io

import time
import numpy as np

from PythonCode.Search.SimulateDynamics import bni_find, fitness_function
from PythonCode.Search.SearchNetwork import SearchNetwork


def get_coupling_value(net):
    return bni_find(net)


def run_search_experiment(net):
    sn = SearchNetwork("NSGA2", network=net, timesteps=4000000)
    res = sn.search(50, 10)
    print("Nodes")
    for nlist in res.X:
        node_indexes = [i for i, x in enumerate(nlist) if x]
        print(node_indexes)
    return res


def search():
    net = io.loadmat('resources\\net_sf_dir_1.mat')['net']
    res = run_search_experiment(net)
    return res


def run_speed_experiment(N, mask, w, net, t):
    seconds = np.zeros((N, 1))
    for i in range(N):
        start_time = time.perf_counter()
        fitness = fitness_function(mask, w, net, t)
        end_time = time.perf_counter()
        seconds[i] = end_time - start_time
    return seconds


def speed():
    N = 1
    mask = np.zeros((200, 20))
    net = io.loadmat('resources\\net_sf_dir_1.mat')['net']
    timesteps = 4000000
    w = get_coupling_value(net)[0][0]
    print(w)
    timings = run_speed_experiment(N, mask, w, net, timesteps)
    print(timings)
    print(np.mean(timings))
    print(np.std(timings))


def test_fitness():
    N = 1
    mask = np.zeros((200, 59))
    net = io.loadmat('resources\\net.mat')['net']
    population_size = 200
    timesteps = 4000000
    w = 213.6953
    timings = run_speed_experiment(1, mask, w, net, timesteps)
    print(timings)


if __name__ == "__main__":
    # speed()
    # test_fitness()
    res = search()
