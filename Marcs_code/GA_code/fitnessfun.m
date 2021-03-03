function y = fitnessfun(x, w, net)
%FITNESSFUN Multi-objective fitness function for the optimisation of the
%removal combination of an epileptic network.
%
% Syntax:  y = fitnessfun(x, w, net)
%
% Inputs:
%    x                  - Binary matrix with size (population size) x (network size).
%                         Each row corresponds to a different individual and each 
%                         column to a node of the network. 1 stands for removal and 
%                         0 for maintenance of the node. 
%    w                  - coupling value for which BNI=0.5 
%    net                - network adjacency matrix
%
% Outputs:
%    y                  - A matrix with the fitness values. Its size is (population size) x 2.
%                         Each row corresponds to a different individual and the two
%                         columns stand for the objective functions. The 1st column
%                         returns the sum of the resected nodes and the 2nd column gives the 
%                         1-DBNI values.
%
% Example:
%    y = fitnessfun(x, w, net)
%    This example calculates the fitness values for the individual x.
%
% Other m-files required: DeltaBNI_r_dir
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
datetime('now')

%count the number of individuals
pop_size = size(x,1);

%allocate a matrix for the output
y = ones(pop_size,2);

%allocate a matrix for the output
y1 = ones(pop_size,1);

%allocate a matrix for the output
y2 = ones(pop_size,1);

%% Calculate the fitness for each individual
for count_indiv = 1:pop_size
    individ = x(count_indiv,:);
    
    %1st objective function : number of resections
    y1(count_indiv) = sum(individ); 

    %2nd objective function : DeltaBNI (We want to maximize DBNI, but 
    %we put 1-DeltaBNI because the algorithm minimizes the obejctive functions)
    y2(count_indiv) = 1-DeltaBNI_r_dir(y1(count_indiv), individ,w,net); 

    
    
end

%% Set values to the return value
y(:,1) = y1;
y(:,2) = y2;

datetime('now')

end

