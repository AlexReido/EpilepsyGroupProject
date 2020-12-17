import random as rand
import numpy as np


"""
Determine if a graph is connected

:param adj: adjacency matrix
:returns S: True if connected, False if not connected
"""
def isconnected_graph(adj):
    if np.count_nonzero(np.sum(adj, axis=0) == 0) != 0:
        return False

    n = len(adj)
    x = np.zeros(n)
    x[0] = 1

    while True:
        y = x
        x = np.matmul(adj, x) + x
        x = x > 0

        if (x == y).all:
            break

    S = True
    if sum(x) < n:
        S = False
    return S

"""
:param n: The number of nodes the network should contain.
:param c: The average degree of each node.
:param gamma: Exponent.
:returns net: The adjacency matrix of the network.
"""
def generate_sf_undir_network(n, c, gamma):
    k = c / 2

    net = 0
    count = 0
    while not isconnected_graph(net) and count < 1000:
        net = sf_und(n, k, gamma)
        count = count + 1
    return net


"""
This function generates an undirected scale-free network.

:param n: number of nodes
:param k: mean degree/2
:param gamma: exponent, smaller the exponent, the more hetrogenous the network is
:returns net: adjacency matrix
"""
def sf_und(n, k, gamma):
    alpha = 1 / (gamma - 1)
    p = np.arange(1, n + 1, 1)
    p = p ** (-alpha)
    p = p / sum(p)
    net = np.zeros((n, n))

    for z in range(1, int(k * n)):
        aux = True
        while aux:
            i = round(rand.random() * (n - 1))
            j = round(rand.random() * (n - 1))
            if net[i, j] == 0 and i != j:
                if p[i] > rand.random() and p[j] > rand.random():
                    net[i, j] = 1
                    net[j, i] = 1
                    aux = False
    return net
