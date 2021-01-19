import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
from scipy import io

import SimulateDynamics
from Tests import TEST_CONSTANTS


def send_to_C(t, wnet, nodes, x, rand_i_sig):
    lib = ctypes.cdll.LoadLibrary("C_code/ctest.so")
    fun = lib.cfun
    fun.restype = None
    fun.argtypes = [ctypes.c_int,  # t
                    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),  # wnet
                    ctypes.c_int,  # nodes
                    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),  # x
                    ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]  # rand_i_sig
    fun(t, wnet, nodes, x, rand_i_sig)

    #return x


if __name__ == "__main__":
    mat_contents = io.loadmat('resources\\net.mat')  # load marc's network
    net = mat_contents[TEST_CONSTANTS.NETWORK_NAME]
    nodes = len(net)  # number of nodes
    w = 25
    timesteps = 4000000
    nodes_resected = 0

    print(SimulateDynamics.theta_model_p(net, 25, 0, t=timesteps))
