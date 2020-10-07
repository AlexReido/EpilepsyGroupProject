function net=sf_und(n,k,gamma)
% This function generates an undirected scale-free network
% Call: net=sf_und(n,c,gamma)
% Input: 
%   n     = number of nodes
%   k     = mean degree/2
%   gamma = exponent
% Output:
%   net   = adjacency matrix
%
% M.A.Lopes @ 2017
 
alpha=1/(gamma-1);
p=(1:n).^(-alpha);
p=p/sum(p);
net=zeros(n);
for z=1:k*n
    aux=1;
    while(aux)
        i=round(rand*(n-1)+1);
        j=round(rand*(n-1)+1);
        if net(i,j)==0 && i~=j
            if p(i)>rand && p(j)>rand
                net(i,j)=1;
                net(j,i)=1;
                aux=0;
            end
        end
    end
end