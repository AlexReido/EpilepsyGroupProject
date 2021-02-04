# import bct
import typer
from PythonCode.GenerateArtificial.GenerateModel import get_artificial_net


# from .PythonCode.GenerateArtificial.GenerateModel import get_artificial_net

def getnetwork(type):
    nodes = 10
    edges = 30
    net = get_artificial_net(nodes, edges, type)
    # print(net)
    return net


def main(type: str):
    network = getnetwork(type)
    typer.echo(network)


if __name__ == "__main__":
    typer.run(main)
