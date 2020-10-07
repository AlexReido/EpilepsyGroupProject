function A=small_world_dir(N,c,p)
% This function generates directed small-world networks.
%
% Call function:
%               A=small_world_dir(N,c,p)
%
% Inputs:
%         N = number of nodes
%         c = mean in and out degree
%         p = probability of rewiring
%
% Output:
%         A = adjacency matrix
%
% M.A.Lopes @ 2017
 
A=zeros(N);
% 1. Construct directed ring
for ii=1:N
    if ii+c<=N
        A(ii,ii+1:ii+c)=1;
    else
        for j=1:c
            if j+ii>N
                A(ii,j+ii-N)=1;
            else
                A(ii,j+ii)=1;
            end
        end
    end
end
 
if p>0 && p<1 % 2. Rewiring    
    L=round(p*sum(sum(A)));
    remove=zeros(L,2);
    add=zeros(L,2);
    net_aux=A;
    count=0;
    while count<=L
        index = round(1+(N-1)*rand(4,1));        
        if net_aux(index(1),index(2))==1 && net_aux(index(3),index(4))==0
            count=count+1;
            remove(count,:)=[index(1),index(2)];            
            add(count,:)=[index(3),index(4)];
            net_aux(index(1),index(2))=2;
            net_aux(index(3),index(4))=2;
        end
    end
    for ii=1:L
        A(remove(ii,1),remove(ii,2))=0;
        A(add(ii,1),add(ii,2))=1;
    end
elseif p==1
    while 1
        A=rand(N)<c/N;
        if mean(sum(A))==c
            break;
        end
    end
end
for ii=1:N % No self-loops 
    if A(ii,ii)==1
       A(ii,ii)=0;       
       while 1
           index = round(1+(N-1)*rand(2,1));
           if A(index(1),index(2))==0 && index(1)~=index(2)
               A(index(1),index(2))=1;
               break;
           end
       end
        
    end
end