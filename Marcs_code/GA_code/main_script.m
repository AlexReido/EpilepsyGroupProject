
%========================================================================================================================================
%This file computes the optimal sets (i.e. the set with the highest Set Ictogenicity) of a network
%across various resection sizes. When you execute it you will obtain Set
%Ictogenicity (SI)  as a function of the resection size
%This code was used in the paper Laiou et al.2019 

%IMPORTANT NOTES!
% 1) You will need to install Matlab coder  
%
% 2) once you install it then you have to execute the function convert2mex.m in
% order to obtain  the mex files (you do it only once). We used the mex files in order to make the scripts with the differential equations faster. 
% Note that the mex files are different in linux/windows so you cannot use the same mex files if you
% use laptops with different operating system
%
% 3) Note that we use parfor (parallel computing) to obtain the results faster 

% For queries with regard to the code you can contact Petroula Laiou (p.laiou@exeter.ac.uk, petroula.laiou@kcl.ac.uk)
%========================================================================================================================================

clear 

%% set parameters
num_gen = 100; %number of generations
pop_size = 200; %population size in each generation

num_GA_runs = 1; %number of GA runs

%% load the network

load('net_sf_dir_1')

%first check if the network has ones in its main diagonal (if yes we delete them)
length_net = length(net);
if diag(net) == ones(length_net, 1)
    net = net-eye(length_net);
end

%% compute the reference coupling value, for which BNI = 0.5

[ref_coupling, BNI_test_values, coupling_test_values] = BNI_find(net);

%% apply the GA 

for count_runs = 1:num_GA_runs
    optimrun(num_gen, pop_size, count_runs, net, ref_coupling)
end

%% plot the results

%From the optimrun function it will be produced a mat file with the name
%out_results_(count_runs).mat

%the suggested nodes are in all_solutions.Xga

%the Set Ictogenciity results are in all_solutions.Fga (1st column: resection size, 2nd column 1-DBNI values)
%Note that the function returns 1-DBNI because NSGA2 minimises the fitness
%functions and does not maximise them
% Therefore if you want to plot the DBNI values versus resection size you have to take
% plot(all_solutions.Fga(:,1), 1-all_solutions.Fga(:,2)). You can also use
% the function sort to sort them in an ascending order






