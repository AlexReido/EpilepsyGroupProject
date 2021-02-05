import unittest
from random import randint

import numpy as np
from numba import jit
from scipy import io
from scipy.special import erfinv

import PythonCode.Search.SimulateDynamics
import TEST_CONSTANTS


def generate_fitness_matrix(population_size, nodes):
    return np.full((population_size, nodes), randint(0, 1))


def randn2(*args, **kwargs):
    '''
    Calls rand and applies inverse transform sampling to the output.
    Used to generate exact same random numbers as the reference matlab implementation
    '''
    uniform = np.random.rand(*args, **kwargs)
    return np.sqrt(2) * erfinv(2 * uniform - 1)


@jit(nopython=True, nogil=True, cache=True, fastmath=True)
def seed_numba(seed):
    np.random.seed(seed)


class TestSimulateDynamics(unittest.TestCase):

    def setUp(self):
        np.random.seed(TEST_CONSTANTS.SEED)  # seed to produce 1.3736e-04 for 'net' with randn2
        mat_contents = io.loadmat(TEST_CONSTANTS.NETWORK_LOCATION)  # load marc's network
        self.network = mat_contents[TEST_CONSTANTS.NETWORK_NAME]
        self.population_size = TEST_CONSTANTS.POPULATION_SIZE

    def tearDown(self):
        self.network = None

    def test_theta_model_p(self):
        w = TEST_CONSTANTS.GLOBAL_COUPLING
        num_nodes_resected = 0  # test for BNI of whole network
        t = TEST_CONSTANTS.TIME_STEPS
        bni = PythonCode.theta_model_p(self.network, w, num_nodes_resected, t)
        self.assertEqual(TEST_CONSTANTS.BNI_RANDN_NUMBA, bni)
        # TODO test with different w values and nodes resected values

    def test_bni_find(self):
        t = TEST_CONSTANTS.FAST_TIME_STEPS
        ref_coupling, BNI_test_values, coupling_test_values = SD.bni_find(self.network, t)
        self.assertEqual(TEST_CONSTANTS.REF_COUPLING, ref_coupling[0])
        # TODO failing

    def test_ref_bni(self):
        w = np.array([[25], [50], [100], [200], [225], [237.5], [250], [300]], dtype=object)
        bni = np.array([[0], [0], [0], [0.012], [0.3228178], [0.48294068], [0.50860593], [0.62369492], [0.74772881]],
                       dtype=object)
        ref = TEST_CONSTANTS.REFERENCE_BNI
        w_ref = SD.ref_bni(w, bni, ref)
        self.assertEqual(w_ref[0], TEST_CONSTANTS.W_REF)

    def test_fitness_function(self):
        t = 4000
        w = 245.8085685983158
        contents = io.loadmat('..\\resources\\x.mat')
        x = contents['r']
        y = SD.fitness_function(x, w, self.network, t, self.seed)
        self.assertEqual(len(y), len(self.network))
        # TODO devise a better test
        # possible accuracy error when comparing to matlab
        self.assertEqual(True, False)  # deliberate failure to highlight lack of testing here


"""
    def test_optimrun(self):
        self.assertEqual(True, False)

    def test_delta_bni_r_dir(self):
        self.assertEqual(True, False)
"""

if __name__ == '__main__':
    unittest.main()