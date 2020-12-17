import math
import numpy as np
import random as rand
from PythonCode.GenerateNetsMarc import generate_sf_undirected_network


def delta_bni_r_dir(num_resect_nodes, individ, w, net):
    """
    delta_bni calculation for a specific network topology.

    :param num_resect_nodes: The number of resected nodes.
    :param individ: A binary array that corresponds to an individual (1 for secting the node, 0 for keeping the node)
    :param w: The coupling value for which BNI=0.5.
    :param net: Network topology

    :returns delta_bni: delta_bni of the network for the specific resection as specified by the individ
    """
    # prepare support data structures

    # Number of runs for the noise of SDEs
    n_n = 5

    # Allocate delta_bni matrix: (1 x noise realiz)
    delta_bni = np.ones(1, n_n)

    # Erase from the network the columns and rows that correspond to the resected nodes

    # Finds the position of the nodes that will be resected
    resected_position = np.where(individ)

    # Remove lines for the resected nodes
    net[resected_position, :] = []

    # Remove columns from the resected nodes
    net[:, resected_position] = []

    # Calculate delta_bni for different noise runs
    for noise in range(n_n):
        delta_bni[0, noise] = (0.5 - theta_model_p(net, w, num_resect_nodes)) / 0.5

    # Set value to the return value
    # Calculate the mean across the noise runs
    delta_bni = np.mean(delta_bni)
    return delta_bni


def fitness_function(x, w, net):
    """
    Multi-objective fitness function for the optimisation of the removal combination of an epileptic network.

    :param x: Binary matrix with size (population size) x (network size). Each row corresponds to a different individual
    and each column to a node of the network. 1 stands for removal and 0 for maintenance of the node.
    :param w: Coupling value for which BNI=0.5
    :param net: Network adjacency matrix
    :returns y: A matrix with the fitness values. Its size is (population size) x 2. Each row corresponds to a different
    individual and the two columns stand for the objective functions. The 1st column returns the sum of the resected
    nodes and the 2nd column gives the 1-DBNI values.
    """
    # count the number of individuals
    pop_size = len(x)

    # allocate a matrix for the output
    y = np.ones(pop_size, 2)

    # allocate a matrix for the output
    y1 = np.ones(pop_size)

    # allocate a matrix for the output
    y2 = np.ones(pop_size)

    # calculate the fitness for each individual
    for count_indiv in range(pop_size):
        individ = x[count_indiv, :]

        # 1st objective function : number of resections
        y1[count_indiv] = sum(individ)

        # 2nd objective function : DeltaBNI (We want to maximize DBNI, but
        # we put 1-DeltaBNI because the algorithm minimizes the objective functions)
        y2[count_indiv] = 1 - delta_bni_r_dir(y1[count_indiv], individ, w, net)

        # Set values to the return value
        y[:, 0] = y1
        y[:, 1] = y2
    return y


def theta_model_p(net, w, nodes_resected):
    """
    This function calculates bni.

    :param net: connectivity matrix NxN
    :param w: global coupling (scalar)
    :param nodes_resected: the number of nodes that are resected
    :returns bni: bni of the network.
    """
    # Fixed Parameters
    t = 4*10**6  # time steps
    i_0 = -1.2  # distance to SNIC
    i_sig = 5 * 1.2 * 0.1  # noise level
    dt = 10**-2  # time step for the integration
    threshold = 0.9  # threshold for bni
    window_epochs = 6*4/dt  # window for bni

    i_sig = i_sig / math.sqrt(dt)
    nodes = len(net)  # number of nodes
    i_0 = i_0 * np.ones(nodes)

    # normalisation of coupling
    wnet = w * net / (nodes + nodes_resected)
    wnet = wnet.conjugate().T

    # allocate matrices and set the values of the theta model for the integration with Euler-Maruyama
    bni = np.zeros(nodes)
    signal = np.zeros(nodes)
    x = np.zeros((t, nodes), dtype=bool)
    theta_s = -np.real(np.arccos([np.divide(1+i_0), (1-i_0)]))  # stable point if i_0 < 0
    theta_old = theta_s  # initial condition

    # Compute time series
    for time in range(t-1):
        ictogenicity = i_0 + i_sig * np.random.rand(nodes, 1) + wnet * (1 - np.cos(theta_old - theta_s))
        theta_new = theta_old + dt * np.multiply(1 - np.cos(theta_old) + (1+np.cos(theta_old)), ictogenicity)
        signal[0, :] = 0.5 * (1 - np.cos(theta_old - theta_s))
        x[time, :] = signal > threshold
        theta_old = theta_new

    # Compute bni
    for node in range(nodes):
        aux = np.where(x[:, node])
        if np.size(aux) == 0:
            bni[node, 0] = 0
        else:
            seizure_index = np.zeros(len(aux), 2)
            seizure_index[0, 0] = aux[0]
            k = 1
            for i in range(1, len(aux)):
                if aux[i] - aux[i-1] > window_epochs:
                    seizure_index[k, 1] = aux[i-1]
                    k += 1
                    seizure_index[k, 0] = aux[i]

            seizure_index[k, 1] = aux[-1]
            seizure_index[k+1:-1, :] = []
            time_seizure = 0
            for i in range(np.size(seizure_index, 0)):
                time_seizure = time_seizure + seizure_index[i, 1] - seizure_index[i, 0] + 1
            bni[node, 0] = time_seizure / t
    bni = np.mean(bni)
    return bni


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
        bni_aux = bni
        bni_aux[bni < ref] = 0
        ind2 = np.argmin(abs(bni_aux-ref))
    else:
        ind2 = ind
        bni_aux = bni
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

        w_ref = (ref-b) / m
    return w_ref


def bni_find(net):
    """
    Calculates the coupling value for which bni = 0.5.

    :param net: The (NxN) functional network. net(i,j) should denote the connection from node i to node j.
    :returns w_ref: The coupling value for which bni = 0.5.
    :returns BNI_test_values: The bni values that calculated while we were searching for the ref_coupling.
    :returns w_safe: The coupling values that correspond to the BNI_test_values.
    """
    # Fixed Parameters
    # TODO move into constants file
    n_n = 5  # runs for noise
    nodes = len(net)  # number of nodes
    w = 25  # initial guess of coupling
    n_max = 50  # max number of attempts
    criteria = 0.05  # criteria for the tuning
    bni_ref = 0.5  # reference of bni we are looking for
    displacement = 0.01  # displacement to help find bni_ref
    num_nodes_resected = 0  # we do not resect nodes because at this stage we want bni of the whole network

    # main calculations
    it = 0
    z = True
    x1 = 0
    x2 = 0
    bni = np.zeros((nodes, n_n, n_max))
    w_save = np.zeros(n_max)

    while z:
        for noise in range(0, n_n):
            bni[:, noise, it] = theta_model_p(net, w, num_nodes_resected)
        it += 1

        w_save[it] = w
        bni_aux1 = np.squeeze(np.mean(np.mean(bni[:, :, it]), 2))
        bni_aux2 = np.squeeze(np.mean(np.mean(bni[:, :, 1:it]), 2))
        print("Iteration: ", it, " | bni = ", bni_aux1, " | w = ", w)

        if it == 1:
            # Lucky guess:
            if criteria > bni_aux1 - bni_ref > 0:
                x1 = 1
            if criteria > bni_ref - bni_aux1 > 0:
                x2 = 1

            if bni_aux1 < bni_ref:
                w *= 2
            else:
                w /= 2
        else:
            # 1st: Find a point above and below bni_ref
            l1 = sum(bni_aux2 > bni_ref)
            l2 = sum(bni_aux2 < bni_ref)
            if (l1 * l2) == 0:
                if bni_aux1 < bni_ref:
                    w *= 2
                else:
                    w /= 2
            # 2nd: Fine tuning
            if criteria > bni_aux1 - bni_ref > 0:
                x1 = 1
            if criteria > bni_ref - bni_aux1 > 0:
                x2 = 1
            bni_aux3, index = np.sort(bni_aux2)
            # ind1 = find(bni_aux3 < bni_ref, 1, 'last')
            ind1 = np.where(bni_aux3 < bni_ref, 1, 'last')
            # ind2 = find(bni_aux3 > bni_ref, 1)
            ind2 = np.where(bni_aux3 > bni_ref, 1)

            slope = (bni_aux3[ind2] - bni_aux3[ind1]) / (w_save[index[ind2]] - w_save[index[ind1]])
            yy0 = bni_aux3[ind2] - slope * w_save[index[ind2]]
            if x1 == 1:
                w = (bni_ref - displacement - yy0) / slope
            elif x2 == 1:
                w = (bni_ref + displacement - yy0) / slope
            else:
                w = (bni_ref - yy0) / slope

        if x1 + x2 == 2 or it == n_max:
            z = False

    w_save[it + 1:-1] = []
    bni[:, :, it + 1:-1] = []

    # calculate the exact coupling value for which bni=0.5
    w, i_w = np.sort(w_save)
    bni = np.squeeze(np.mean(np.mean(bni), 2))
    w_ref = ref_bni(w, bni[i_w], 0.5)
    bni_test_values = bni

    return w_ref, bni_test_values, w_save


def optimrun(generations, population, work_item, net, w):
    """
    Main function of the epileptic network optimisation method.

    :param generations: NSGA-II generations number.
    :param population: NSGA-II population size.
    :param work_item: NSGA-II work_item name.
    :param net: Network Topology.
    :param w: The coupling value for which BNI = 0.5.
    """
    # Network size in nodes
    nodes = len(net)
    rand.seed('shuffle')

    # Create struct to save individuals of each generation
    all_solutions = []
    # All solutions.target.ts = target_ts
    all_solutions.generations = 1

    # Set NSGA-II fitness function and parameters
    # fitfunc = (x)fitnessfun(x, w, net)

    # NSGA-II parameters
    #optGA = gaoptimset

    # start profiler parameters
    #ga_start = tic

    # Execute the NSGA-II


# set parameters
num_gen = 100  # number of generations
pop_size = 200  # population size in each generation
num_GA_runs = 1  # number of GA runs

# create the network
n = 20
c = 2
gamma = 3
network = generate_sf_undirected_network(n, c, gamma)
print(network)

# first check if the network has ones in its main diagonal (if yes we delete them)
length_net = len(network)
if (np.diag(network) == np.ones((length_net, 1))).all:
    network = network - np.eye(length_net)

# compute the reference coupling value, for which BNI = 0.5
ref_coupling, BNI_test_values, coupling_test_values = bni_find(network)

# apply the GA
for count_runs in range(num_GA_runs):
    optimrun(num_gen, pop_size, count_runs, network, ref_coupling)
