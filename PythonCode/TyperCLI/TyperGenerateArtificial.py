import typer
from PythonCode.GenerateArtificial.GenerateModel import get_artificial_net


def getnetwork(type, nodes, edges):
    net = get_artificial_net(nodes, edges, type)
    # print(net)
    return net


def main(
        type: str = typer.Argument(..., help="Type of structural network: random, lattice or toeplitz"),
        n: int = typer.Option(10, help="Number of nodes in network"),
        e: int = typer.Option(30, help="Number of edges in network")
):
    """
    Generate a network based on the type and optional nodes and edges provided \n
    Type should be either random, lattice or toeplitz. \t
    Prints network to console.
    """
    network = getnetwork(type, n, e)
    typer.echo(network)


if __name__ == "__main__":
    typer.run(main)
