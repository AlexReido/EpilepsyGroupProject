import unittest
from math import isclose

import numpy as np
from scipy import io
from PythonCode.Search.SimulateDynamics import bni_find, ref_bni, theta_model_p, fitness_function, delta_bni_r_dir
import TEST_CONSTANTS
from PythonCode.Tests.helper_test_functions import randn2


class TestSimulateDynamics(unittest.TestCase):

    def setUp(self):
        np.random.seed(TEST_CONSTANTS.SEED)  # seed to produce 1.3736e-04 for 'net' with randn2
        mat_contents = io.loadmat(TEST_CONSTANTS.NETWORK_LOCATION)  # load marc's network
        self.network = mat_contents[TEST_CONSTANTS.NETWORK_NAME]
        self.population_size = TEST_CONSTANTS.POPULATION_SIZE

    def tearDown(self):
        self.network = None

    def test_theta_model_p(self):
        t = TEST_CONSTANTS.TIME_STEPS
        w = 25
        num_nodes_resected = 0  # test for BNI of whole network

        bni = theta_model_p(self.network, w, num_nodes_resected, t)
        self.assertTrue(isclose(TEST_CONSTANTS.BNI_RANDN_MAT, bni, abs_tol=0.0001))  # for when testing with MATLAB random numbers

        w = 213.4872  # coupling value for this network
        bni = theta_model_p(self.network, w, num_nodes_resected, t)
        self.assertTrue(isclose(TEST_CONSTANTS.BNI_RANDN_COUPLING_MAT, bni, abs_tol=0.1))  # to within accuracy measure

        num_nodes_resected = 5  # test for BNI when nodes have been resected
        bni = theta_model_p(self.network, w, num_nodes_resected, t)
        self.assertTrue(isclose(TEST_CONSTANTS.BNI_RANDN_COUPLING_RESECTED_MAT, bni, abs_tol=0.1))  # to within accuracy measure

    def test_bni_find(self):
        t = TEST_CONSTANTS.TIME_STEPS
        # 213.5789963246309 with 4,000,000 timesteps
        ref_coupling, BNI_test_values, coupling_test_values = bni_find(self.network, t)
        self.assertTrue(isclose(TEST_CONSTANTS.REF_COUPLING, ref_coupling[0], abs_tol=0.1))

    def test_ref_bni(self):
        w = np.array([[25], [50], [100], [200], [225], [237.5], [250], [300]], dtype=np.float64)
        bni = np.array([[0], [0], [0], [0.012], [0.3228178], [0.48294068], [0.50860593], [0.62369492], [0.74772881]], dtype=np.float64)
        ref = TEST_CONSTANTS.REFERENCE_BNI
        w_ref = ref_bni(w, bni, ref)
        self.assertTrue(isclose(w_ref[0], TEST_CONSTANTS.W_REF, abs_tol=0.01))
        # TODO needs test for when bni < ref

    def test_delta_bni_r_dir(self):
        num_resect_nodes = 0
        individ = np.zeros((len(self.network), 1))
        w = 213.6953
        delta_bni = delta_bni_r_dir(num_resect_nodes, individ, w, self.network)
        self.assertTrue(isclose(0.0, delta_bni, abs_tol=0.01))

        individ = np.zeros((len(self.network), 1))
        individ[0, 0] = 1
        individ[len(self.network)-1, 0] = 1
        num_resect_nodes = 2
        w = 213.6953
        delta_bni = delta_bni_r_dir(num_resect_nodes, individ, w, self.network)
        self.assertTrue(isclose(-0.01, delta_bni, abs_tol=0.01))

    def test_fitness_function(self):
        w = 213.6953
        x = np.zeros((200, len(self.network)))
        y = fitness_function(x, w, self.network)
        self.assertEqual(200, len(y))
        self.assertTrue(isclose(200, sum(y[:, 1]), abs_tol=1))

if __name__ == '__main__':
    unittest.main()