clear all


% Parameters:
N = 20; % number of nodes
c = 2;  % mean degree (should be an even integer)
 
 
% ------------------------
% 1. Undirected networks -
% ------------------------
 
% 1a. Small-world, lattice, and random networks 
p = 1; % re-wiring probability
% p = 0 corresponds to a lattice; p = 1 is a random network
 
net=0;
while(~isconnected_graph(net)) % to avoid disconnected graphs    
    net=small_world_und(N,c/2,p);
end
  
figure(1) % Visualize the network
subplot 121
imagesc(net)
 
subplot 122
plot(graph(net))



% save([pwd '/', 'net_r_undir_10.mat'], 'net')

%savedir = '/Users/plaiou/Desktop/EDK_DSE_Xm/directed/in_out_degree_2/generate_networks_BNIcurves/';
%filename = sprintf('net_sf_dir_1');
%save([savedir, filename], 'net')
