import unittest
from math import isclose, sqrt

import numpy as np
from scipy import io
from scipy.special import erfinv
import PythonCode.SimulateDynamics as SD


def randn2(*args, **kwargs):
    '''
    Calls rand and applies inverse transform sampling to the output.
    Used to generate exact same random numbers as the reference matlab implementation
    '''
    uniform = np.random.rand(*args, **kwargs)
    return sqrt(2) * erfinv(2 * uniform - 1)


class TestSimulateDynamics(unittest.TestCase):

    def setUp(self):
        self.seed = 1337
        np.random.seed(self.seed)  # seed to produce 1.3736e-04 for 'net' with randn2
        mat_contents = io.loadmat('..\\resources\\net.mat')  # load marc's network
        self.network = mat_contents['net']

    def tearDown(self):
        self.network = None

    def test_theta_model_p(self):
        w = 25
        num_nodes_resected = 0  # test for BNI of whole network
        t = 4 * 10 ** 6
        bni = SD.theta_model_p(self.network, w, num_nodes_resected, t, seed=self.seed)
        # self.assertEqual(bni, 0.00013736016949152544)  # when using randn2
        self.assertEqual(bni, 0.00014334745762711868)  # when using np.random.randn
"""
    def test_bni_find(self):
        t = 4000 # would take too long if 4000000
        seed = 1337
        ref_coupling, BNI_test_values, coupling_test_values = SD.bni_find(self.network, t=t, seed=seed)
        self.assertEqual(ref_coupling[0], 245.8085685983158)

    def test_ref_bni(self):
        w = np.array([[25], [50], [100], [200], [225], [237.5], [250], [300]], dtype=object)
        bni = np.array([[0], [0], [0], [0.012], [0.3228178], [0.48294068], [0.50860593], [0.62369492], [0.74772881]], dtype=object)
        ref = 0.5
        w_ref = SD.ref_bni(w, bni, ref)
        self.assertEqual(w_ref[0], 245.8085689794567)


    def test_delta_bni_r_dir(self):
        self.assertEqual(True, False)

    def test_fitness_function(self):
        self.assertEqual(True, False)

    def test_optimrun(self):
        self.assertEqual(True, False)
"""

if __name__ == '__main__':
    unittest.main()
