from scipy import io
import numpy as np
import pandas as pd


def calc_adjMatrix(iEEG):
    df = pd.DataFrame(iEEG)
    return np.asarray(df.corr(method="pearson"))


def get_channels(mat_contents, var):
    return mat_contents[var]


def convert(mat_contents, var):
    iEEG = get_channels(mat_contents, var)
    adj = calc_adjMatrix(iEEG)
    return adj


def get_adjacency(data):
    """ Converts string from matlab file
        :returns the adjacency matrix as a numpy array"""
    f = open("..\\resources\\curr_network.mat", "w")
    f.write(data)
    f.close()
    adj = convert(io.loadmat('..\\resources\\curr_network.mat'), 'data')
    return adj

if __name__ == "__main__":
    data = []
    get_adjacency(data)

