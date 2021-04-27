import io
from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
from pymoo.factory import get_performance_indicator


def extract_result(res):
    node_nums = res.F[:, 0]
    bni_vals = res.F[:, 1]
    return node_nums, bni_vals


def plot_pareto_front(data):
    """

    :param data: a Nx2 matrix, first column is resected nodes, second column SI score.
    :param generations: number of generations used for the search algorithm.
    :param pop_size: population sized used for the search algorithm.
    :param algorithm: the search algorithm used.
    """
    # x = [len(data[i, 0]) for i in range(len(data[:, 0]))]
    x = [x[0] for x in data]
    y = [x[1] for x in data]

    plt.title("Set Ictogenicity vs Number of Resected Nodes")
    plt.xlabel("Number of nodes resected")
    plt.ylabel("Set Ictogenicity")
    plt.scatter(x, y)
    plt.show()

    #plt.savefig("curr_pareto_front", dpi=300)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # use
    # im = Image.open(buffer)
    # OR imgplt = plt.imshow(plt.imread(buffer))
    # im.show()
    # buf.close()
    return buffer


def plot_adj(net, data):
    """
    Plot the adjacency heatmap of the resected networks.

    :param net: The original network.
    :param data: An Nx2 matrix, first column is resected nodes as a binary encoding, second column is SI score.
    """

    plt.imshow(net)
    cbar = plt.colorbar()
    cbar.set_ticks([0,1])
    cbar.ax.set_yticklabels(['Zero', 'One'],)
    cbar.set_label('link', rotation=270)
    plt.xlabel('node index')
    plt.ylabel('node index')
    plt.show()
    plt.savefig("unmodified_network", dpi=300)

    for i in range(len(data[:, 0])):
        resected_position = np.where(data[i, 0] == 0)
        resected_net = net[:, resected_position[0]]
        resected_net = resected_net[resected_position[0], :]

        plt.imshow(resected_net)
        plt.savefig("resected_network_" + str(i+1), dpi=300)


def hypervolume(res, net):
    ref_point = np.array([1.1 * len(net), 1.1])
    hv = get_performance_indicator("hv", ref_point=ref_point)
    return hv.calc(res)