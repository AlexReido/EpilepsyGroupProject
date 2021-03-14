from random import randint
import numpy as np
from scipy.special import erfinv


def generate_fitness_matrix(population_size, nodes):
    return np.full((population_size, nodes), randint(0, 1))


def randn2(*args, **kwargs):
    '''
    Calls rand and applies inverse transform sampling to the output.
    Used to generate exact same random numbers as the reference matlab implementation
    '''
    uniform = np.random.rand(*args, **kwargs)
    return np.sqrt(2) * erfinv(2 * uniform - 1)