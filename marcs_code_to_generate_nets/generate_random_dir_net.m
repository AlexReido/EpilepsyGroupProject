clear all
% 2a. Small-world, lattice, and random networks 
%p = 0.1; % re-wiring probability
% p = 0 corresponds to a lattice; p = 1 is a random network

%define parameters

p = 1;%re-wiring probability for random networks
c = 2;% Note that in directed networks, 'c' is the mean in- and out-degree
N = 20;%nodes of the netwrok


bins=2;
while max(bins)>1 % to avoid disconnected graphs
    net=small_world_dir(N,c,p);
    G=digraph(net);
    bins = conncomp(G,'Type','weak');
end
 
figure % Visualize the network
subplot 121
imagesc(net)
 
subplot 122
plot(digraph(net))


% save([[pwd '/', 'net_r_dir_10.mat']], 'net')
