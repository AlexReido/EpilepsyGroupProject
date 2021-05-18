function DeltaBNI = DeltaBNI_r_dir(num_resect_nodes, individ, w, net)
%DELTABNI_R_DIR DeltaBNI calculation for a specific network topology.
%
% Syntax:  y = DeltaBNI_r_dir(x, w, net)
%
% Inputs:
%    num_resect_nodes   - The number of resected nodes
%    individ            - A binary array that corresponds to an individual 
%                         (1 for secting the node, 0 for keeping the node)
%    w                  - The coupling value for which BNI=0.5
%    net                - Network topology
%
% Outputs:
%    DeltaBNI           - DeltaBNI of the network for the specific 
%                         resection as specified by the individ
%
% Example:
%    y = DeltaBNI_r_dir(2, [1 1 0 0], w, net)
%    This example calculates the DeltaBNI for a network with 2 removed
%    nodes.
%
% Other m-files required: theta_model_P_mex, theta_model_P
% Subfunctions: none
% MAT-files required: none
%
% See also: Goodfellow, M., Rummel, C., Abela, E., Richardson, M. P., 
% Schindler, K., & Terry, J. R. (2016). Estimation of brain network 
% ictogenicity predicts outcome from epilepsy surgery. Scientific Reports, 
% 6(1), 29215. https://doi.org/10.1038/srep29215
%
% @author: Petroula Laiou $
% @email: P.Laiou@exeter.ac.uk  $
% @date: 05/12/2017 $
% @version: 1.0 $
% @copyright: Not specified

%% Prepare support data structures

% Number of runs for the noise of SDEs
n_n = 5;

% Allocate DeltaBNI matrix: (1 x noise realiz)
DeltaBNI = ones(1, n_n);

%% Erase from the network the columns and rows that correspond to the resected nodes  

% Finds the position of the nodes that will be resected
resected_position = find(individ);

% Remove lines for the resected nodes
net(resected_position, :) = [];
% Remove columns for the resected nodes
net(:,resected_position) = [];

%% Calculate DeltaBNI for different noise runs
% Replace parfor with for to run the loop using one thread.
for noise=1:n_n
    DeltaBNI(1,noise)=(0.5-theta_model_P_mex(net, w, num_resect_nodes))/0.5;
    %it also runs with (0.5-theta_model_P_mex(net,w, num_resect_nodes))/0.5; but it is much slower
%     sprintf('nodesresected_%0.0f_noise_realiz%0.0f', num_resect_nodes, noise)
end

%% Set value to the return value
% Calculate the mean across the noise runs
DeltaBNI = mean(DeltaBNI); 

end

