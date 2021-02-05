from GenerateArtificial import GenerateModel
import bct

from Search.SearchNetwork import SearchNetwork


def getnetwork(type):
    nodes = 10
    edges = 30
    net = GenerateModel.getStructuralnetwork(nodes, edges, type)
    # print(net)
    return net


if __name__ == '__main__':
    print("Random Network")
    rand = getnetwork("random")
    d = bct.distance_wei_floyd(rand)
    print(d[0])
    net = d[0]
    # TODO assert first two returned equal in unit tests
    # if (d[0] == d[1]).all():
    #     print("EQUAL")

    net = GenerateModel.postProcessing(net)
    print(net)
    sn = SearchNetwork("NSGA2", net,400000)
    sn.search(50)
    print("=======================================================")
    #
    # print("Lattice Network")
    # latt = getnetwork("lattice")
    # distance = bct.distance_wei_floyd(latt)
    # print(d[0])
    # # if (d[0] == d[1]).all():
    # #     print("EQUAL")
    # print("=======================================================")
    #
    # print("Toeplitz Network")
    # toe = getnetwork("toeplitz")
    # d = bct.distance_wei_floyd(toe)
    # print(d[0])
    # # if (d[0] == d[1]).all():
    # #     print("EQUAL")
    # print("=======================================================")

    # numpy.ndarray