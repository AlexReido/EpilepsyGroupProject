function [ref_coupling, BNI_test_values, coupling_test_values] = BNI_find(net)

% This function calculates the coupling value for which BNI = 0.5;
% It is a modification of the BNI_find function from Marinho Lopes (Group methods)
% version:1, Petroula Laiou,  06/01/2018

%INPUT
% - net: The (NxN) functional network. 
%        net(i,j) should denote the connection from node i to node j
%
%OUTPUT
% - ref_coupling: the coupling value for which BNI = 0.5
% - BNI_test_values: The BNI values that calculated while we were searching for
%                    the ref_coupling
% - coupling_test_values: The coupling values that correspond to the
%                         BNI_test_values
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Fixed parameters:
n_n=5;            % runs for noise
N=length(net);    % number of nodes
w=25;             % initial guess of coupling 
n_max=50;         % max number of attempts
crit=0.05;        % criteria for the tuning
BNI_ref=0.5;      % reference of BNI we are looking for
displac=0.01;        % displacement to help find BNI_ref
num_nodes_resected = 0; %we do not resect modes because at this stage we want BNI of the whole network

%% main calculations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%if exist('BNI_aux.mat','file')==0
%    it=0;
%    z=1;
%    x1=0;
%    x2=0;
%    BNI=zeros(N,n_n,n_max);
%    w_save=zeros(n_max,1);
%else
%    load('BNI_aux.mat');
%end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

it=0;
z=1;
x1=0;
x2=0;
BNI=zeros(N,n_n,n_max);
w_save=zeros(n_max,1);

while(z)
    it=it+1;
    parfor noise=1:n_n
        BNI(:,noise,it)=theta_model_P_mex(double(net),w,num_nodes_resected);
    end
    w_save(it)=w;
    bni_aux1=squeeze(mean(mean(BNI(:,:,it)),2));
    bni_aux2=squeeze(mean(mean(BNI(:,:,1:it)),2));
    disp(['Iteration: ' num2str(it) ' | BNI = ' num2str(bni_aux1) ' | w = ' num2str(w)]);
    if it==1
        % Lucky guess:        
        if bni_aux1-BNI_ref<crit && bni_aux1-BNI_ref>0
            x1=1;
        end
        if BNI_ref-bni_aux1<crit && BNI_ref-bni_aux1>0 
            x2=1; 
        end       

        if bni_aux1<BNI_ref
            w=w*2;
        else
            w=w/2;
        end

    else
        % 1st: Find a point above and below BNI_ref
        L1=sum(bni_aux2>BNI_ref);
        L2=sum(bni_aux2<BNI_ref);        
        if L1*L2==0
            if bni_aux1<BNI_ref
                w=w*2;
            else
                w=w/2;
            end
            continue;
        end
        % 2nd: Fine tuning
        if bni_aux1-BNI_ref<crit && bni_aux1-BNI_ref>0
            x1=1;            
        end
        if BNI_ref-bni_aux1<crit && BNI_ref-bni_aux1>0
            x2=1;            
        end        
        [bni_aux3,index]=sort(bni_aux2);       
        ind1=find(bni_aux3<BNI_ref,1,'last');
        ind2=find(bni_aux3>BNI_ref,1);

        slope=(bni_aux3(ind2)-bni_aux3(ind1))/(w_save(index(ind2))-w_save(index(ind1)));
        yy0=bni_aux3(ind2)-slope*w_save(index(ind2));
        if x1==1
            w=(BNI_ref-displac-yy0)/slope;
        elseif x2==1
            w=(BNI_ref+displac-yy0)/slope;
        else
            w=(BNI_ref-yy0)/slope;
        end 

    end    
    if (x1+x2==2 || it==n_max)
        z=0;
    end
    save('BNI_aux.mat','BNI','w_save','w','it','z','x1','x2','-v7.3');
end

w_save(it+1:end)=[];
BNI(:,:,it+1:end)=[];

%% calculate the exact coupling value for which BNI=0.5
        
[w, i_w] = sort(w_save);
bni = squeeze(mean(mean(BNI),2));
w_ref=ref_bni(w,bni(i_w),0.5);
ref_coupling = w_ref;

BNI_test_values = BNI;
coupling_test_values = w_save;

delete('BNI_aux.mat');
 
 
end
       

