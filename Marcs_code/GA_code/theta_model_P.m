function BNI=theta_model_P(net,w,nodes_resected)
%This function calculates BNI. This function is slightely modified from the
%function theta_model (Marinho Lopes-group methods)
% version:1, Petroula Laiou,  06/01/2018

%INPUT: 
% -net            : connectivity matrix NxN 
% -w              : global coupling (scalar)
% -nodes_resected : the number of nodes that are resected

%OUTPUT:
% -BNI            : BNI of the network

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%rng('shuffle');it is not supported for the convertion to the mex files

% Fixed parameters:
T = 4000;         % time steps
I_0 = -1.2;         % distance to SNIC
I_sig = 5*1.2*0.1;  % noise level
dt = 10^-2;         % time step for the integration
threshold = 0.9;    % threshold for BNI
window_epochs = 6*4/dt; % window for BNI


I_sig = I_sig/sqrt(dt); 
N = length(net); % number of nodes
I_0 = I_0*ones(N,1);

% normalisation of coupling
wnet = w*net/(N+nodes_resected);
wnet = wnet';

%allocate matrices and set the values of the theta model for the integration
%with Euler-Maruyama

BNI = zeros(N,1);
signal = zeros(1,N);
x = false(T,N);
theta_s = -real(acos((1+I_0)./(1-I_0))); % stable point if I_0 < 0
theta_old = theta_s; % initial condition  

%rng(1337)

% Compute time series
for time = 1:T-1
    I = I_0+I_sig*randn2(N,1)+wnet*(1-cos(theta_old-theta_s));
    theta_new = theta_old+dt*(1-cos(theta_old)+(1+cos(theta_old)).*I);
    s = 0.5*(1-cos(theta_old-theta_s));
    signal(1,:) = s;
    x(time+1,:) = signal>threshold;
    theta_old = theta_new;
end

% Compute BNI
for node = 1:N
    aux = find(x(:,node));
    if numel(aux) == 0
        BNI(node,1) = 0;
    else
        seizure_index = zeros(length(aux),2);
        seizure_index(1,1) = aux(1);
        k = 1;
        for i = 2:length(aux)
            if aux(i)-aux(i-1)>window_epochs
                seizure_index(k,2) = aux(i-1);
                k = k+1;
                seizure_index(k,1) = aux(i);
            end
        end
        seizure_index(k,2) = aux(end);
        seizure_index(k+1:end,:) = [];
        time_seizure = 0;
        for i = 1:size(seizure_index,1)
            time_seizure = time_seizure+seizure_index(i,2)-seizure_index(i,1)+1;
        end
        BNI(node,1) = time_seizure/T;
    end
end

BNI = mean(BNI);

end
