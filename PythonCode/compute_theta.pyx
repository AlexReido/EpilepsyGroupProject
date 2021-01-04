#cython: -c=-DUSE_XSIMD -c=-march=native
#cython: cxx=True

import numpy as np
cimport numpy as cnp
cimport cython


ctypedef cnp.float_t DTYPE_t
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def compute_theta(int t, cnp.ndarray[DTYPE_t, ndim=2] wnet, float dt, int nodes, float threshold):
    cdef float i_sig = 5.0 * 1.2 * 0.1  # noise level
    cdef float dist = -1.2  # distance to SNIC
    i_sig = i_sig / np.sqrt(dt)

    # Compute time series
    cdef cnp.ndarray[cnp.float_t, ndim=2] rand_i_sig = (i_sig * np.random.randn(t, nodes)).transpose()  # transpose to give same values as matlab
    cdef cnp.ndarray[cnp.float_t, ndim=3] theta = np.empty((t, 59, 1), dtype=np.float)
    cdef cnp.ndarray[cnp.float_t, ndim=2] i_0 = np.full((nodes, 1), dist, dtype=float)
    theta[0, :] = -np.real(np.arccos(np.divide(1 + i_0, 1 - i_0)))  # stable point if i_0 < 0

    cdef cnp.ndarray[cnp.float_t, ndim=2] cos_theta_old
    cdef cnp.ndarray[cnp.float_t, ndim=2] ictogenicity

    cdef Py_ssize_t time
    for time in range(1, t):

        cos_theta_old = np.cos(theta[time - 1, :], dtype=float)
        ictogenicity = i_0 + rand_i_sig[:, time - 1:time] + np.dot(wnet, 1 - np.cos(theta[time - 1, :] - theta[0, :]))
        theta[time, :] = theta[time - 1, :] + np.dot(dt, (1 - cos_theta_old + ((1 + cos_theta_old) * ictogenicity)))

    return np.squeeze(1 - np.cos(theta - theta[0, :])) * 0.5 > threshold