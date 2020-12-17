import math
import numpy as np
import random as rand

from PythonCode.generate_nets_marc import generate_sf_undir_network

"""
DeltaBNI calculation for a specific network topology.

:param num_resect_nodes: The number of resected nodes.
:param individ: A binary array that corresponds to an individual (1 for secting the node, 0 for keeping the node)
:param w: The coupling value for which BNI=0.5.
:param net: Network topology

:returns DeltaBNI: DeltaBNI of the network for the specific resection as specified by the individ
"""
def DeltaBNI_r_dir(num_resect_nodes, individ, w, net):
    # prepare support data structures

    # Number of runs for the noise of SDEs
    n_n = 5

    # Allocate DeltaBNI matrix: (1 x noise realiz)
    DeltaBNI = np.ones(1, n_n)

    # Erase from the network the columns and rows that correspond to the resected nodes

    # Finds the position of the nodes that will be resected
    resected_position = np.where(individ)

    # Remove lines for the resected nodes
    net[resected_position, :] = []

    # Remove columns from the resected nodes
    net[:, resected_position] = []

    # Calculate DeltaBNI for different noise runs
    for noise in range(n_n):
        DeltaBNI[0, noise] = (0.5 - theta_model_P(net, w, num_resect_nodes))/0.5

    # Set value to the return value
    # Calculate the mean across the noise runs
    DeltaBNI = np.mean(DeltaBNI)
    return DeltaBNI


"""
Multi-objective fitness function for the optimisation of the removal combination of an epileptic network.

:param x: Binary matrix with size (population size) x (network size). Each row corresponds to a different individual and 
each column to a node of the network. 1 stands for removal and 0 for maintenance of the node.
:param w: Coupling value for which BNI=0.5
:param net: Network adjacency matrix
:returns y: A matrix with the fitness values. Its size is (population size) x 2. Each row corresponds to a different 
individual and the two columns stand for the objective functions. The 1st column returns the sum of the resected nodes
and the 2nd column gives the 1-DBNI values.
"""
def fitnessfun(x, w, net):
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
        y2[count_indiv] = 1 - DeltaBNI_r_dir(y1[count_indiv], individ, w, net)

        # Set values to the return value
        y[:, 0] = y1
        y[:, 1] = y2
    return y


"""
This function calculates BNI.

:param net: connectivity matrix NxN
:param w: global coupling (scalar)
:param nodes_resected: the number of nodes that are resected
:returns BNI: BNI of the network.
"""
def theta_model_P(net, w, nodes_resected):
    # Fixed Parameters
    T = 4*10**6  # time steps
    I_0 = -1.2  # distance to SNIC
    I_sig = 5 * 1.2 * 0.1  # noise level
    dt = 10**-2  # time step for the integration
    threshold = 0.9  # threshold for BNI
    window_epochs = 6*4/dt  # window for BNI

    I_sig = I_sig / math.sqrt(dt)
    N = len(net) # number of nodes
    I_0 = I_0 * np.ones(N)

    # normalisation of coupling
    wnet = w * net / (N + nodes_resected)
    wnet = wnet.conjugate().T

    # allocate matrices and set the values of the theta model for the integration with Euler-Maruyama
    BNI = np.zeros(N)
    signal = np.zeros(N)
    x = np.zeros((T, N), dtype=bool)
    theta_s = -np.real(np.arccos([np.divide(1+I_0), (1-I_0)]))  # stable point if I_0 < 0
    theta_old = theta_s # initial condition

    # Compute time series
    for time in range(T-1):
        I = I_0 + I_sig * np.random.rand(N, 1) + wnet * (1 - np.cos(theta_old - theta_s))
        theta_new = theta_old + dt * np.multiply(1 - np.cos(theta_old) + (1+np.cos(theta_old)), I)
        signal[0, :] = 0.5 * (1 - np.cos(theta_old - theta_s))
        x[time, :] = signal > threshold
        theta_old = theta_new

    # Compute BNI
    for node in range(N):
        aux = np.where(x[:, node])
        if np.size(aux) == 0:
            BNI[node, 0] = 0
        else:
            seizure_index = np.zeros(len(aux), 2)
            seizure_index[0,0] = aux[0]
            k = 1
            for i in range(1, len(aux)):
                if aux[i] - aux[i-1] > window_epochs:
                    seizure_index[k,1] = aux[i-1]
                    k += 1
                    seizure_index[k,0] = aux[i]

            seizure_index[k,1] = aux[-1]
            seizure_index[k+1:-1, :] = []
            time_seizure = 0
            for i in range(np.size(seizure_index, 0)):
                time_seizure = time_seizure + seizure_index[i, 1] - seizure_index[i, 0] + 1
            BNI[node, 0] = time_seizure / T
    BNI = np.mean(BNI)
    return BNI


"""
This function calculates the weight w_ref at which BNI=ref.
:param w: The coupling value for which BNI=0.5.
param BNI: The brain network ictogenicity values.
param ref: The reference value of BNI to achieve.
:returns w_ref: The coupling value for which BNI = 0.5.
"""
def ref_bni(w, BNI, ref):
    err = 0.00001
    ind = np.argmin(abs(BNI-ref))
    if BNI[ind] < ref:
        ind1 = ind
        BNI_aux = BNI
        BNI_aux[BNI<ref] = 0
        ind2 = np.argmin(abs(BNI_aux-ref))
    else:
        ind2 = ind
        BNI_aux = BNI
        BNI_aux[BNI > ref] = 0
        ind1 = np.argmin(abs(BNI_aux - ref))

    x1 = w[ind1]
    y1 = BNI[ind1]
    x2 = w[ind2]
    y2 = BNI[ind2]

    if abs(x1 - x2) < err:
        w_ref = x1
    else:
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        w_ref = (ref-b) / m
    return w_ref


"""
Calculates the coupling value for which BNI = 0.5.

:param net: The (NxN) functional network. net(i,j) should denote the connection from node i to node j.
:returns ref_coupling: The coupling value for which BNI = 0.5.
:returns BNI_test_values: The BNI values that calculated while we were searching for the ref_coupling.
:returns coupling_test_values: The coupling values that correspond to the BNI_test_values.
"""
def BNI_find(net):
    # Fixed Parameters
    # TODO move into constants file
    n_n = 5  # runs for noise
    N = len(net)  # number of nodes
    w = 25  # initial guess of coupling
    n_max = 50  # max number of attempts
    crit = 0.05  # criteria for the tuning
    BNI_ref = 0.5  # reference of BNI we are looking for
    displac = 0.01  # displacement to help find BNI_ref
    num_nodes_resected = 0  # we do not resect nodes because at this stage we want BNI of the whole network

    # main calculations
    it = 0
    z = True
    x1 = 0
    x2 = 0
    BNI = np.zeros((N, n_n, n_max))
    w_save = np.zeros(n_max)

    while z:
        for noise in range(0, n_n):
            BNI[:, noise, it] = theta_model_P(net, w, num_nodes_resected)
        it += 1

        w_save[it] = w
        bni_aux1 = np.squeeze(np.mean(np.mean(BNI[:, :, it]), 2))
        bni_aux2 = np.squeeze(np.mean(np.mean(BNI[:, :, 1:it]), 2))
        print("Iteration: ", it, " | BNI = ", bni_aux1, " | w = ", w)

        if it == 1:
            # Lucky guess:
            if crit > bni_aux1 - BNI_ref > 0:
                x1 = 1
            if crit > BNI_ref - bni_aux1 > 0:
                x2 = 1

            if bni_aux1 < BNI_ref:
                w *= 2
            else:
                w /= 2
        else:
            # 1st: Find a point above and below BNI_ref
            L1 = sum(bni_aux2 > BNI_ref)
            L2 = sum(bni_aux2 < BNI_ref)
            if (L1 * L2) == 0:
                if bni_aux1 < BNI_ref:
                    w *= 2
                else:
                    w /= 2
            # 2nd: Fine tuning
            if crit > bni_aux1 - BNI_ref > 0:
                x1 = 1
            if crit > BNI_ref - bni_aux1 > 0:
                x2 = 1
            bni_aux3, index = np.sort(bni_aux2)
            # ind1 = find(bni_aux3 < BNI_ref, 1, 'last')
            ind1 = np.where(bni_aux3 < BNI_ref, 1, 'last')
            # ind2 = find(bni_aux3 > BNI_ref, 1)
            ind2 = np.where(bni_aux3 > BNI_ref, 1)

            slope = (bni_aux3[ind2] - bni_aux3[ind1]) / (w_save[index[ind2]] - w_save[index[ind1]])
            yy0 = bni_aux3[ind2] - slope * w_save[index[ind2]]
            if x1 == 1:
                w = (BNI_ref - displac - yy0) / slope
            elif x2 == 1:
                w = (BNI_ref + displac - yy0) / slope
            else:
                w = (BNI_ref - yy0) / slope

        if x1 + x2 == 2 or it == n_max:
            z = False

    w_save[it + 1:-1] = []
    BNI[:, :, it + 1:-1] = []

    # calculate the exact coupling value for which BNI=0.5
    w, i_w = np.sort(w_save)
    bni = np.squeeze(np.mean(np.mean(BNI), 2))
    w_ref = ref_bni(w, bni[i_w], 0.5)
    ref_coupling = w_ref

    BNI_test_values = BNI
    coupling_test_values = w_save

    return ref_coupling, BNI_test_values, coupling_test_values


"""
Main function of the epileptic network optimisation method.

:param generations: NSGA-II generations number.
:param population: NSGA-II population size.
:param work_item: NSGA-II work_item name.
:param net: Network Topology.
:param w: The coupling value for which BNI = 0.5.
"""
def optimrun(generations, population, work_item, net, w):
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
net = generate_sf_undir_network(n, c, gamma)
print(net)

# first check if the network has ones in its main diagonal (if yes we delete them)
length_net = len(net)

if (np.diag(net) == np.ones((length_net, 1))).all:
    net = net - np.eye(length_net)

# compute the reference coupling value, for which BNI = 0.5
ref_coupling, BNI_test_values, coupling_test_values = BNI_find(net)

# apply the GA
for count_runs in range(num_GA_runs):
    optimrun(num_gen, pop_size, count_runs, net, ref_coupling)
