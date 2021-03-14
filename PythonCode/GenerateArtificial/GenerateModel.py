import warnings

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import bct
import numpy as np
#import matlab.engine
from numpy import inf

app = FastAPI()


def symmetrize(a):
    """
    Return a symmetrized version of NumPy array a.

    Values 0 are replaced by the array value at the symmetric
    position (with respect to the diagonal), i.e. if a_ij = 0,
    then the returned array a' is such that a'_ij = a_ji.

    Diagonal values are left untouched.

    a -- square NumPy array, such that a_ij = 0 or a_ji = 0,
    for i != j.
    """
    return a + a.T - np.diag(a.diagonal())


def getStructuralnetwork(k, m, structure):
    """
    Generates a structural network based on the structure provided using the bct toolbox
    :param k: number of nodes
    :param m: number of edges
    :param structure:
    :return: the structural adjacency matrix where an edge between nodes is denoted with a 1 and no edge 0
    """
    if structure == "random":
        return symmetrize(bct.makerandCIJ_und(k, m))
    elif structure == "lattice":
        return bct.makeringlatticeCIJ(k, m)
    elif structure == "toeplitz":
        # TODO check on toeplitz edges as too high fails e.g. 10 nodes with 60 edges fails
        return bct.maketoeplitzCIJ(k, m, 1.5).astype(float)
    elif structure == "smallword":
        return True  # TODO small world
    else:
        raise ValueError("Network type: " + type + "not supported")


def postProcessing(net):
    # values inversely proportional to distance
    # the divide by zero produces a warning but is dealt with so we ignore them
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        net = np.divide(0.01, net)
    # infinite distance set to value zero as no connection between nodes
    net[net == inf] = 0
    # Add noise to matrix
    noise = np.random.normal(0.002, 0.001, len(net))
    net = net - noise
    net[net < 0] = 0
    return net


def get_artificial_net(k, m, structure):
    net = getStructuralnetwork(k, m, structure)
    # print(net)
    d = bct.distance_wei_floyd(net)
    net = d[0]
    net = postProcessing(net)
    return net


@app.get("/model/artificial/")
async def generateNetwork(nodes: int = 20, edges: int = 100, structure: str = "random"):
    # weighted undirected network
    model = getStructuralnetwork(nodes, edges, structure)
    # functional = bct.motif3funct_bin(model)
    distance = bct.distance_wei_floyd(model, 'log')
    # print("ditancee:")
    # print(type(distance))
    # print(distance)
    # print("first")
    print(distance[2])
    print(model)
    max = np.amax(distance)
    # print(max)
    # transform = lambda x: x/max
    func = np.divide(distance, max)
    func = np.around(func, 3)
    # print(func)
    # eng = matlab.engine.start_matlab()
    # print(type(model))
    # print(type(func))
    # print(type(distance))
    # # SC FC ED pred_var model
    predvar = ['ED']  # ,'SPLwei_log','SI','T']
    # predvar = matlab.double(predvar)
    # bct.z
    # res = eng.predict_fc(matlab.double(model.tolist()), matlab.double(func.tolist()),
    #                      matlab.double(distance[2].tolist()), predvar, nargout=5)
    # print(res)
    # functionalConnectivity = bct.p
    # print(functional)
    # print(type(model))
    listmodel = func.tolist()
    return listmodel[2]
