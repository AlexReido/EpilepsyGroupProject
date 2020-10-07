clear all
rng('shuffle')
N = 20;
c = 2;

% 1b. Scale-free networks 
gamma = 3;  % exponent (should be >= 2)
% the smaller the exponent, the more heterogenous is the network
 
net=0;count=0;
while(~isconnected_graph(net)&&count<1000) % to avoid disconnected graphs 
    net=sf_und(N,c/2,gamma);
    count=count+1; % a connected network might not exist! 
end
 
figure(2) % Visualize the network
subplot 121
imagesc(net)
 
subplot 122
plot(graph(net))

% save([pwd '/', 'net_sf_undir_10.mat'], 'net')