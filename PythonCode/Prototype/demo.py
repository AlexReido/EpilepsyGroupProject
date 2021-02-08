import numba as nb
import numpy as np
from scipy import io

from PythonCode import CONSTANTS
from PythonCode.Tests.test_fitness import randn2


@nb.jit(nopython=True, nogil=True, cache=True, fastmath=True)
def numba_compute_theta(t, wnet, nodes, rand_i_sig):
    """
    Compute the time series using the Euler-Maruyama method.
    This method uses the numba library for JIT.

    :param rand_i_sig:
    :param t: time steps.
    :param wnet: normalisation of coupling.
    :param dt: time step for the integration.
    :param nodes: number of nodes in the network.
    :param threshold: threshold value for BNI.
    :param seed: seed to control random number distribution.
    :return: time series of the network.
    """

    theta = np.empty((t, nodes, 1))
    theta[0, :] = -np.real(np.arccos(np.divide(1 + CONSTANTS.DIST, 1 - CONSTANTS.DIST)))  # stable point if i_0 < 0

    for time in np.arange(1, t):
        cos_theta_old = np.cos(theta[time - 1, :])
        ictogenicity = rand_i_sig[:, time - 1:time] + (wnet @ (1 - np.cos(
            theta[time - 1, :] - theta[0, :])))
        theta[time, :] = theta[time - 1, :] + (
                    CONSTANTS.DT * (1 - cos_theta_old + ((1 + cos_theta_old) * ictogenicity)))

    return (1 - np.cos(theta - theta[0, :]))[:, :, 0] * 0.5 > CONSTANTS.THRESHOLD  # squeeze not supported by numba


@nb.jit(parallel=True, nopython=True, nogil=True, cache=True, fastmath=True)
def theta_model_p(net, w, nodes_resected, rand_i_sig, t=4000000):
    """
    This function calculates bni.

    :param net: connectivity matrix NxN
    :param w: global coupling (scalar)
    :param nodes_resected: the number of nodes that are resected
    :param t: time steps
    :param seed: seed to control random number distribution
    :returns bni: bni of the network.
    """
    nodes = len(net)  # number of nodes

    # normalisation of coupling
    wnet = w * net / (nodes + nodes_resected)
    wnet = np.ascontiguousarray(wnet.conj().T)  # Complex conjugate transpose

    # allocate matrices and set the values of the theta model for the integration with Euler-Maruyama
    bni = np.zeros((nodes, 1))
    x = numba_compute_theta(t, wnet, nodes, rand_i_sig)  # python with numba library (fastest)

    # Compute bni
    for node in range(nodes):
        aux = np.flatnonzero(x[:, node])  # move outside loop
        if len(aux) == 0:
            bni[node, 0] = 0
        else:
            seizure_index = np.zeros((len(aux), 2))  # 2 is a dimension for new array
            seizure_index[0, 0] = aux[0]
            k = 0
            for i in range(1, len(aux)):
                if aux[i] - aux[i - 1] > CONSTANTS.WINDOW_EPOCHS:
                    seizure_index[k, 1] = aux[i - 1]
                    k += 1
                    seizure_index[k, 0] = aux[i]

            seizure_index[k, 1] = aux[-1]
            seizure_index = seizure_index[:k+1:]
            time_seizure = 0
            for i in range(seizure_index.shape[0]):
                time_seizure = time_seizure + seizure_index[i, 1] - seizure_index[i, 0] + 1
            bni[node, 0] = time_seizure / t

    return np.mean(bni)


if __name__ == "__main__":
    # Final product will not include tests so best avoid importing from folder
    import PythonCode.Tests.TEST_CONSTANTS as TEST_CONSTANTS

    np.random.seed(1337)
    mat_contents = io.loadmat(TEST_CONSTANTS.NETWORK_LOCATION)  # load marc's network
    network = mat_contents[TEST_CONSTANTS.NETWORK_NAME]

    t = 4000000
    nodes = 59
    i_sig = CONSTANTS.NOISE / np.sqrt(CONSTANTS.DT)

    rand_i_sig = i_sig * randn2(t, nodes).transpose() + CONSTANTS.DIST

    bni = theta_model_p(network, 25, 0, rand_i_sig, 4000000)
    print(bni)
