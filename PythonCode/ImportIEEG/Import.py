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


if __name__ == "__main__":
    mat_contents = io.loadmat('..\\resources\\HUP064_sz_1.mat')  # load marc's network
    adj = convert(mat_contents, 'data')
    print(adj)

