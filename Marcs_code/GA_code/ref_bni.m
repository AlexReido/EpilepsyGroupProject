function w_ref=ref_bni(w,BNI,ref)
% This function calculates the weight w_ref at which BNI=ref.
% How to use it: w_ref=ref_bni(w,BNI,ref)
% This is a function from Marinho Lopes (group Methods)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

err=0.00001;
[~,ind]=min(abs(BNI-ref));
if BNI(ind)<ref
    ind1=ind;
    BNI_aux=BNI;
    BNI_aux(BNI<ref)=0;
    [~,ind2]=min(abs(BNI_aux-ref));
else
    ind2=ind;
    BNI_aux=BNI;
    BNI_aux(BNI>ref)=0;
    [~,ind1]=min(abs(BNI_aux-ref));
end

x1=w(ind1);
y1=BNI(ind1);
x2=w(ind2);
y2=BNI(ind2);

if abs(x1-x2)<err
    w_ref=x1;
else
    m=(y2-y1)/(x2-x1);
    b=y1-m*x1;
    
    w_ref=(ref-b)/m;
end