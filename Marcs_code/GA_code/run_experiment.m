function times = run_experiment(N, mask, net)

%[ref_coupling, BNI_test_values, coupling_test_values] = BNI_find(net);

times = NaT(N, 2);
times(1, 1) = datetime();
fitnessfun(mask, 213.6953, net);
times(1, 2) = datetime();

%for i=1:N
%    times(i,1) = datetime();
%    fitness = fitnessfun(reshape(x(i,:,:),200,20), ref_coupling, net);
%    times(i,2) = datetime();
%end