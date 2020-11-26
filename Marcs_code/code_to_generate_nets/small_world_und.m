function net = small_world_und(N,K,p)
% This function generates undirected binary small-world netwoks.
%
% Call function:
%    net = small_world_und(N,K,p)
% Inputs:
%   N = number of nodes
%   K = mean degree / 2
%   p = rewiring probability
%
% p = 0 is a ring lattice, and p = 1 is a random graph.
 
% Connect each node to its K next and previous neighbors. 
% This constructs indices for a ring lattice.
s = repelem((1:N)',1,K);
t = s + repmat(1:K,N,1);
t = mod(t-1,N)+1;
 
% Rewire the target node of each edge with probability p
for source=1:N    
    switchEdge = rand(K, 1) < p;
     
    newTargets = rand(N, 1);
    newTargets(source) = 0;
    newTargets(s(t==source)) = 0;
    newTargets(t(source, ~switchEdge)) = 0;
     
    [~, ind] = sort(newTargets, 'descend');
    t(source, switchEdge) = ind(1:nnz(switchEdge));
end
 
h = graph(s,t);
net = full(adjacency(h));
end