import typer
from PythonCode.Search.SearchNetwork import SearchNetwork
import numpy as np
from scipy import io


def loadnetwork(fname):
    """
    Loads the network from file in same folder
    :param fname:
    :return:
    """

class SearchWProgress():
    # def __init__(self) -> None:
    def nextgeneration(self):
        self.progress.update(1)

    def dosearch(self, searcher, gen, n):
        with typer.progressbar(length=gen,  label="Genetic search") as self.progress:
            results = searcher.search(gen, n, self)
        return results

def main(
        algorithm: str = typer.Argument("NSGA2", help="Search algorithm used: NSGA2 or MOEAD"),
        t: int = typer.Option(4000000, help="Number of time steps in euler method"),
        n: int = typer.Option(10, help="Maximum number of nodes to be selected for resection"),
        f: str = typer.Option(None, help="The file name of the network"),
        gen: int = typer.Option(30, help="Number of generations")
):
    """
    Search a network based on the type and optional nodes and edges provided \n
    Type should be either random, lattice or toeplitz. \t
    Prints network to console.
    """
    if f !=None:
        net = np.load(f +".npy")
    else:
        net = io.loadmat('../resources/net.mat')
        net = net['net']

    searcher = SearchNetwork(algorithm, network=net, timesteps=t)
    swp = SearchWProgress()

    results = swp.dosearch(searcher, gen, n)
    typer.echo(results.F)
    typer.echo(results.X)


if __name__ == "__main__":
    typer.run(main)
