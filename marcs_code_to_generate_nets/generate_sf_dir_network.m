clear all
rng('shuffle')
N = 20;
c = 2;

bins=2; count=0;
while(max(bins)>1&&count<1000) % to avoid disconnected graphs
    net=BAgraph_dir(N,c,c);
    G=digraph(net);
    bins = conncomp(G,'Type','weak');
    count=count+1; % a connected network might not exist!
end
 
figure(5) % Visualize the network
subplot 121
imagesc(net)
 
subplot 122
plot(digraph(net))



% save([pwd '/', 'net_sf_dir_10.mat'], 'net')

%savedir = '/Users/plaiou/Desktop/EDK_DSE_Xm/directed/in_out_degree_2/generate_networks_BNIcurves/';
%filename = sprintf('net_sf_dir_1');
%save([savedir, filename], 'net')





