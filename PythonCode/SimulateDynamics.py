import numpy as np
from scipy import io
import numba as nb
import PythonCode.CONSTANTS as CONSTANTS
from Tests import TEST_CONSTANTS
# from Tests.test_SimulateDynamics import randn2


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
    i_0 = CONSTANTS.DIST
    initial_theta = -np.real(np.arccos(np.divide(1 + i_0, 1 - i_0)))  # stable point if i_0 < 0
    theta[0, :] = initial_theta

    for time in np.arange(1, t):
        cos_theta_old = np.cos(theta[time - 1, :])
        ictogenicity = i_0 + rand_i_sig[:, time - 1:time] + (wnet @ (1 - np.cos(
            theta[time - 1, :] - theta[0, :])))
        theta[time, :] = theta[time - 1, :] + (
                    CONSTANTS.DT * (1 - cos_theta_old + ((1 + cos_theta_old) * ictogenicity)))

    return (1 - np.cos(theta - theta[0, :]))[:, :, 0] * 0.5 > CONSTANTS.THRESHOLD  # squeeze not supported by numba

# class DynamicsSimulator:
#
#     def __init__(self)

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
    # 95 % of time
    rand_i_sig = i_sig * np.random.randn(nodes, t)
    print(rand_i_sig.shape)
    #rand_i_sig = i_sig * r andn2(t, nodes).transpose()  # transpose to give same values as matlab

    x = numba_compute_theta(t, wnet, nodes, rand_i_sig)  # python with numba library (fastest)

    # Compute bni
    for node in range(nodes):
        aux = np.transpose(np.nonzero(x[:, node]))
        if np.size(aux) == 0:
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
            seizure_index = np.delete(seizure_index, np.s_[k + 1::], 0)
            time_seizure = 0
            for i in range(seizure_index.shape[0]):
                time_seizure = time_seizure + seizure_index[i, 1] - seizure_index[i, 0] + 1
            bni[node, 0] = time_seizure / t

    return np.mean(bni)


def ref_bni(w, bni, ref):
    """
    This function calculates the weight w_ref at which BNI=ref.
    :param w: The coupling value for which BNI=0.5.
    :param bni: The brain network ictogenicity values.
    :param ref: The reference value of BNI to achieve.
    :returns w_ref: The coupling value for which BNI = 0.5.
    """
    err = 0.00001
    ind = np.argmin(abs(bni - ref))
    if bni[ind] < ref:
        ind1 = ind
        bni_aux = np.copy(bni)
        bni_aux[bni < ref] = 0
        ind2 = np.argmin(abs(bni_aux - ref))
    else:
        ind2 = ind
        bni_aux = np.copy(bni)
        bni_aux[bni > ref] = 0
        ind1 = np.argmin(abs(bni_aux - ref))

    x1 = w[ind1]
    y1 = bni[ind1]
    x2 = w[ind2]
    y2 = bni[ind2]

    if abs(x1 - x2) < err:
        w_ref = x1
    else:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        w_ref = (ref - b) / m
    return w_ref


def bni_find(net, t=4000000):
    """
    Calculates the coupling value for which bni = 0.5.

    :param net: The (NxN) functional network. net(i,j) should denote the connection from node i to node j.
    :param t: time steps
    :param seed: seed to control random number distribution
    :returns w_ref: The coupling value for which bni = 0.5.
    :returns BNI_test_values: The bni values that calculated while we were searching for the ref_coupling.
    :returns w_safe: The coupling values that correspond to the BNI_test_values.
    """

    nodes = len(net)  # number of nodes
    w = 25  # initial guess of coupling

    # main calculations
    it = 0
    z = True
    x1 = 0
    x2 = 0
    bni = np.zeros((nodes, CONSTANTS.N_N, CONSTANTS.N_MAX))
    w_save = np.zeros((CONSTANTS.N_MAX, 1))

    while z:
        it += 1
        for noise in range(CONSTANTS.N_N):
            bni[:, noise, it - 1] = theta_model_p(net, w, CONSTANTS.NUM_NODES_RESECTED, t)

        w_save[it - 1] = w
        bni_aux1 = np.mean(np.mean(np.squeeze(bni[:, :, it - 1]), keepdims=True, axis=0), keepdims=True, axis=1)
        bni_aux2 = np.mean(np.mean(np.squeeze(bni[:, :, :it]), keepdims=True, axis=0), axis=1, keepdims=True)
        print("Iteration: ", it, " | bni = ", bni_aux1, " | w = ", w)

        if it == 1:
            # Lucky guess:
            if CONSTANTS.CRITERIA > bni_aux1 - CONSTANTS.BNI_REF > 0:
                x1 = 1
            if CONSTANTS.CRITERIA > CONSTANTS.BNI_REF - bni_aux1 > 0:
                x2 = 1

            if bni_aux1 < CONSTANTS.BNI_REF:
                w *= 2
            else:
                w /= 2
        else:
            # 1st: Find a point above and below bni_ref
            l1 = np.sum(bni_aux2 > CONSTANTS.BNI_REF)
            l2 = np.sum(bni_aux2 < CONSTANTS.BNI_REF)
            if (l1 * l2) == 0:
                if bni_aux1 < CONSTANTS.BNI_REF:
                    w *= 2
                else:
                    w /= 2
                continue
            # 2nd: Fine tuning
            if CONSTANTS.CRITERIA > bni_aux1 - CONSTANTS.BNI_REF > 0:
                x1 = 1
            if CONSTANTS.CRITERIA > CONSTANTS.BNI_REF - bni_aux1 > 0:
                x2 = 1
            bni_aux3 = np.squeeze(np.sort(bni_aux2))
            index = np.squeeze(np.argsort(bni_aux2))
            ind1 = np.nonzero(bni_aux3 < CONSTANTS.BNI_REF)[0][-1]
            ind2 = np.nonzero(bni_aux3 > CONSTANTS.BNI_REF)[0][0]

            slope = (bni_aux3[ind2] - bni_aux3[ind1]) / (w_save[index[ind2]] - w_save[index[ind1]])
            yy0 = bni_aux3[ind2] - slope * w_save[index[ind2]]
            if x1 == 1:
                w = (CONSTANTS.BNI_REF - CONSTANTS.DISPLACEMENT - yy0) / slope
            elif x2 == 1:
                w = (CONSTANTS.BNI_REF + CONSTANTS.DISPLACEMENT - yy0) / slope
            else:
                w = (CONSTANTS.BNI_REF - yy0) / slope

            #  TODO error in reference implementation? w above is redundant
            # w = (w_save[index[ind1]] + w_save[index[ind2]])[0] / 2

        if x1 + x2 == 2 or it == CONSTANTS.N_MAX:
            z = False

    w_save = np.delete(w_save, np.s_[it:], 0)
    bni = bni[:, :, :it]

    # calculate the exact coupling value for which bni=0.5
    w = np.sort(w_save, axis=0)
    i_w = np.argsort(w_save, axis=0)
    bni = np.squeeze(np.mean(np.mean(bni, keepdims=True, axis=0), keepdims=True, axis=1))
    w_ref = ref_bni(w, bni[i_w], 0.5)

    ref_coupling = w_ref
    bni_test_values = bni
    coupling_test_values = w_save

    return ref_coupling, bni_test_values, coupling_test_values


def delta_bni_r_dir(num_resect_nodes, individ, w, net, t=4000000):
    """
    DeltaBNI calculation for the given network.

    :param num_resect_nodes: The number of resected nodes.
    :param individ: A binary array that corresponds to an individual (1 for resecting the node, 0 for keeping the node).
    :param w: The coupling value for which BNI = 0.5.
    :param net: Network.
    :param t: timesteps
    :param seed: controls the random distribution
    :return: DeltaBNI of the network for the specific resection as specified by the individ
    """
    # Allocate delta_bni matrix: (1 x noise realiz)
    delta_bni = np.ones((1, CONSTANTS.N_N))

    # Finds the position of the nodes that will be resected
    resected_position = np.where(individ)

    # Remove rows for the resected nodes
    net = np.delete(net, resected_position[0], axis=0)

    # Remove columns from the resected nodes
    net = np.delete(net, resected_position[0], axis=1)

    # TODO multi thread this loop
    # Calculate delta_bni for different noise runs
    for noise in range(CONSTANTS.N_N):
        delta_bni[0, noise] = (CONSTANTS.DELTA_BNI - theta_model_p(net, w, num_resect_nodes, t=t)) / 0.5

    # Set value to the return value
    # Calculate the mean across the noise runs
    delta_bni = np.mean(delta_bni)
    return delta_bni


def fitness_function(x, w, net, t=4000000):
    """
    Multi-objective fitness function for the optimisation of the removal combination of an epileptic network.

    :param x: Binary matrix with size (population size) x (network size).
              Each row corresponds to a different individual and each column to a node of the network.
              1 stands for removal and 0 for maintenance of the node.
    :param w: coupling value for which BNI=0.5.
    :param net: The network adjacency matrix.
    :param t: The number of time steps.
    :param seed: Controls the random distribution.
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

    # TODO vectorise and multithread loop?
    # Calculate the fitness for each individual
    for count_indiv in range(pop_size):
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

if __name__ == "__main__":
    mat_contents = io.loadmat(TEST_CONSTANTS.NETWORK_LOCATION)  # load marc's network
    network = mat_contents[TEST_CONSTANTS.NETWORK_NAME]
    bni = theta_model_p(network, 25, 0, 4000)