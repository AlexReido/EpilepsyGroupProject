import bct
import typer

import GenerateModel


def getnetwork(type):
    nodes = 10
    edges = 30
    net = GenerateModel.getStructuralnetwork(nodes, edges, type)
    # print(net)
    return net

def realnetwork(network):
    d = bct.distance_wei_floyd(network)
    net = d[0]
    net = GenerateModel.postProcessing(net)
    return net

def main(type: str):
    network = getnetwork(type)
    network = realnetwork(network)
    typer.echo(network)


if __name__ == "__main__":
    typer.run(main)