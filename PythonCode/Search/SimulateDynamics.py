import numpy as np
from numba import prange
from scipy import io
import numba as nb
import PythonCode.CONSTANTS as CONSTANTS
from PythonCode.Tests import TEST_CONSTANTS
from PythonCode.Tests.helper_test_functions import randn2


@nb.jit(nopython=True, nogil=True, cache=True, fastmath=True)
def theta_model_p(net, w, nodes_resected, t=4000000):
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

    # Compute time series
    i_sig = CONSTANTS.NOISE / np.sqrt(CONSTANTS.DT)

    x = np.full((t, nodes), False)
    theta_start = np.empty((1, nodes))
    theta_start[:] = -np.real(np.arccos(np.divide(1 + CONSTANTS.DIST, 1 - CONSTANTS.DIST)))
    theta_old = theta_start

    for time in range(1, t):
        cos_theta_old = np.cos(theta_old)
        ictogenicity = (i_sig * np.random.randn(1, nodes)) + CONSTANTS.DIST + ((1 - np.cos(
            theta_old - theta_start)) @ wnet)
        #ictogenicity = (i_sig * np.random.randn(nodes, 1).T) + CONSTANTS.DIST + ((1 - np.cos(
            #theta_old - theta_start)) @ wnet)
        theta_old = theta_old + (CONSTANTS.DT * (1 - cos_theta_old + ((1 + cos_theta_old) * ictogenicity)))
        x[time, :] = 0.5 * (1 - np.cos(theta_old - theta_start)) > CONSTANTS.THRESHOLD

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
            seizure_index = seizure_index[:k + 1:]
            time_seizure = 0
            for i in range(seizure_index.shape[0]):
                time_seizure = time_seizure + seizure_index[i, 1] - seizure_index[i, 0] + 1
            bni[node, 0] = time_seizure / t

    return np.mean(bni)


@nb.jit(nopython=True, nogil=True, cache=True, fastmath=True)
def ref_bni(w, bni, ref):
    """
    This function calculates the weight w_ref at which BNI=ref.
    :param w: The coupling value for which BNI=0.5.
    :param bni: The brain network ictogenicity values.
    :param ref: The reference value of BNI to achieve.
    :returns w_ref: The coupling value for which BNI = 0.5.
    """
    ind = np.argmin(np.abs(bni - ref))
    if bni[ind] < ref:
        ind1 = ind
        bni_aux = np.copy(bni)

        for i in range(len(bni)):
            if bni[i] < ref:
                bni_aux[i] = 0

        ind2 = np.argmin(np.abs(bni_aux - ref))
    else:
        ind2 = ind
        bni_aux = np.copy(bni)

        for i in range(len(bni)):
            if bni[i] > ref:
                bni_aux[i] = 0

        ind1 = np.argmin(np.abs(bni_aux - ref))

    x1 = w[ind1]
    y1 = bni[ind1]
    x2 = w[ind2]
    y2 = bni[ind2]

    if np.abs(x1 - x2) < CONSTANTS.ERROR:
        w_ref = x1
    else:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        w_ref = (ref - b) / m
    return w_ref


@nb.jit(parallel=True, nopython=True, nogil=True, cache=True, fastmath=True)
def run_theta_calc(bni, it, net, w, t):
    """
    Compute the BNI values for the given coupling value.

    :param bni: The bni values for each coupling value guess.
    :param it: The current iteration.
    :param net: The functional network.
    :param w: The current guess of the coupling value.
    :param t: The number of timesteps.
    :return: The BNI values for the given coupling value.
    """
    for noise in prange(CONSTANTS.N_N):
        bni[it - 1, noise] = theta_model_p(net, w, CONSTANTS.NUM_NODES_RESECTED, t)
    return bni


def bni_find(net, t=4000000):
    """
    Calculates the coupling value for which bni = 0.5.
    Note: DOES NOT REQUIRE NUMBA

    :param net: The (NxN) functional network. net(i,j) should denote the connection from node i to node j.
    :param t: The number of timesteps to use in compute_theta.
    :returns w_ref: The coupling value for which bni = 0.5.
    :returns BNI_test_values: The bni values that calculated while we were searching for the ref_coupling.
    :returns w_safe: The coupling values that correspond to the BNI_test_values.
    """

    nodes = len(net)  # number of nodes
    w = 25  # initial guess of coupling

    # main calculations
    it = 0
    x1 = False
    x2 = False
    bni = np.zeros((CONSTANTS.N_MAX, CONSTANTS.N_N))
    w_save = np.zeros((CONSTANTS.N_MAX, 1))

    while not ((x1 and x2) or it == CONSTANTS.N_MAX):
        it += 1
        w = np.ravel(w)[0]

        bni = run_theta_calc(bni, it, net, w, t)

        w_save[it - 1] = w
        bni_aux1 = np.mean(bni[it-1, :])  # find the mean of the latest row
        bni_aux2 = np.asarray([np.mean(bni[i, :]) for i in range(it)])
        print("Iteration: ", it, " | bni = ", bni_aux1, " | w = ", w)

        if it == 1:
            # Lucky guess:
            if CONSTANTS.CRITERIA > bni_aux1 - CONSTANTS.BNI_REF > 0:
                x1 = True
            if CONSTANTS.CRITERIA > CONSTANTS.BNI_REF - bni_aux1 > 0:
                x2 = True

            if bni_aux1 < CONSTANTS.BNI_REF:
                w *= 2
            else:
                w /= 2
        else:
            # 1st: Find a point above and below bni_ref
            l1 = np.multiply(bni_aux2 > CONSTANTS.BNI_REF, 1)
            l2 = np.multiply(bni_aux2 < CONSTANTS.BNI_REF, 1)
            if np.sum(l1) * np.sum(l2) == 0:
                if bni_aux1 < CONSTANTS.BNI_REF:
                    w *= 2
                else:
                    w /= 2
                continue
            # 2nd: Fine tuning
            if CONSTANTS.CRITERIA > bni_aux1 - CONSTANTS.BNI_REF > 0:
                x1 = True
            if CONSTANTS.CRITERIA > CONSTANTS.BNI_REF - bni_aux1 > 0:
                x2 = True

            bni_aux3 = np.sort(bni_aux2)
            index = np.argsort(bni_aux2, axis=0)

            ind1 = np.flatnonzero(bni_aux3 < CONSTANTS.BNI_REF)[-1]
            ind2 = np.flatnonzero(bni_aux3 > CONSTANTS.BNI_REF)[0]

            slope = (bni_aux3[ind2] - bni_aux3[ind1]) / (w_save[index[ind2]] - w_save[index[ind1]])
            yy0 = bni_aux3[ind2] - slope * w_save[index[ind2]]
            if x1:
                w = (CONSTANTS.BNI_REF - CONSTANTS.DISPLACEMENT - yy0) / slope
            elif x2:
                w = (CONSTANTS.BNI_REF + CONSTANTS.DISPLACEMENT - yy0) / slope
            else:
                w = (CONSTANTS.BNI_REF - yy0) / slope

    w_save = w_save[:it]
    bni = bni[:it, :]

    # calculate the exact coupling value for which bni=0.5
    w = np.sort(w_save.T).T
    i_w = np.argsort(w_save, axis=0)
    bni = np.asarray([np.mean(bni[i, :]) for i in range(it)])
    w_ref = ref_bni(w, bni[i_w], 0.5)

    return w_ref, bni, w_save


@nb.jit(parallel=True, nopython=True, nogil=True, cache=True, fastmath=True)
def delta_bni_r_dir(num_resect_nodes, individ, w, net, t=4000000):
    """
    DeltaBNI calculation for the given network.

    :param num_resect_nodes: The number of resected nodes.
    :param individ: A binary array that corresponds to an individual (1 for resecting the node, 0 for keeping the node).
    :param w: The coupling value for which BNI = 0.5.
    :param net: Network.
    :param t: timesteps.
    :return: DeltaBNI of the network for the specific resection as specified by the individ
    """
    # Allocate delta_bni matrix: (1 x noise realiz)
    delta_bni = np.ones((1, CONSTANTS.N_N))

    # Finds the position of the nodes that will be resected
    resected_position = np.where(individ == 0)

    # Remove rows for the resected nodes
    net = net[:, resected_position[0]]

    # Remove columns from the resected nodes
    net = net[resected_position[0], :]

    # Calculate delta_bni for different noise runs
    for noise in prange(CONSTANTS.N_N):
        delta_bni[0, noise] = (CONSTANTS.DELTA_BNI - theta_model_p(net, w, num_resect_nodes, t=t)) / 0.5

    # Calculate the mean across the noise runs
    return np.mean(delta_bni)


@nb.jit(parallel=True, nopython=True, nogil=True, cache=True, fastmath=True)
def fitness_function(x, w, net, t=4000000):
    """
    Multi-objective fitness function for the optimisation of the removal combination of an epileptic network.

    :param x: Binary matrix with size (population size) x (network size).
              Each row corresponds to a different individual and each column to a node of the network.
              1 stands for removal and 0 for maintenance of the node.
    :param w: coupling value for which BNI=0.5.
    :param net: The network adjacency matrix.
    :param t: The number of time steps.
    :return: A matrix with with the fitness values. Its size is (population size) x2. Each row corresponds to a
             different individual and the two columns stand for the objective functions. The 1st column returns the sum
             of the resected nodes and the 2nd column gives the 1-DBNI values.
    """

    # count the number of individuals
    pop_size = len(x)

    # allocate a matrix for the output
    y = np.ones((pop_size, 2))

    # allocate a matrix for the output
    y1 = np.ones(pop_size)

    # allocate a matrix for the output
    y2 = np.ones(pop_size)

    # Calculate the fitness for each individual
    for count_indiv in prange(pop_size):
        individ = x[count_indiv, :]

        # 1st objective function : number of resections
        y1[count_indiv] = np.sum(individ)

        # 2nd objective function : DeltaBNI (We want to maximize DBNI, but
        # we put 1-DeltaBNI because the algorithm minimizes the objective functions)
        y2[count_indiv] = 1 - delta_bni_r_dir(y1[count_indiv], individ, w, net, t)

    # Set values to the return value
    y[:, 0] = y1
    y[:, 1] = y2
    return y
