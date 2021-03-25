from timeit import default_timer as timer

from scipy import io

from PythonCode.Search.SearchNetwork import SearchNetwork


def run_search(optimiser, timesteps, generations, max_nodes):
    sn = SearchNetwork(optimiser, timesteps=timesteps)
    start = timer()
    res = sn.search(generations, max_nodes)
    end = timer()

    # TODO save time to file
    elapsed = end - start

    # TODO save nodes to file
    print("Nodes")
    for nlist in res.X:
        node_indexes = [i for i, x in enumerate(nlist) if x]
        print(node_indexes)
    return None


if __name__ == "__main__":
    optimiser = "NSGA2"
    timesteps = 4000000
    generations = 100
    population_size = 200
    network = io.loadmat('../resources/net.mat')['net']
    max_nodes = len(network) / 2  # half the number of nodes in network
    run_search(optimiser, timesteps, generations, max_nodes)
