function optimrun(generations, population, work_item, net, w)
%OPTIMRUN Main function of the epileptic network optimisation method. The code
%is based on https://github.com/avramidis/nystagmus-optimisation
%
%
% Syntax:  optimrun(generations, population, work_item, net, w)
%
% Inputs:
%    generations        - NSGA-II generations number
%    population         - NSGA-II population size
%    work_item          - NSGA-II work_item name
%    net                - Network topology
%    w                  - The coupling value for which BNI=0.5
%
% Outputs: 
%    none
%
% Example:
%    optimrun(100, 100, 1, net, w)
%    This example starts a MOGA client.
%
% Other m-files required: fitnessfun.m
% Subfunctions: none
% MAT-files required: none
%
% See also: Goodfellow, M., Rummel, C., Abela, E., Richardson, M. P., 
% Schindler, K., & Terry, J. R. (2016). Estimation of brain network 
% ictogenicity predicts outcome from epilepsy surgery. Scientific Reports, 
% 6(1), 29215. https://doi.org/10.1038/srep29215
% and
% E. Avramidis & O.E. Akman. Optimisation of an exemplar oculomotor model
% using multi-objective genetic algorithms executed on a GPU-CPU combination.
% BMC Syst. Biol., 11: 40 (2017)
%
% @author: Petroula Laiou, Eleftherios Avramidis $
% @email: P.Laiou@exeter.ac.uk el.avramidis@gmail.com $
% @date: 04/12/2017 $
% @version: 1.0 $
% Copyright: Not specified

% Network size in nodes
nodes = size(net,1);

disp(['Current path: ' pwd])
rng('shuffle')
diary('matlog.txt')
diary on

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Delete states results mat file
delete('states.mat')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Delete optimisation results mat file
if exist('all_solutions.mat')==2
    delete('all_solutions.mat');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Output struct
% Create struct to save individuals of each generation
all_solutions = struct();
% all_solutions.target.ts = target_ts;
all_solutions.generations = 1;
save('all_solutions.mat', 'all_solutions');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Set NSGA-II fitness function and parameters

% Fitness function
% fhm=@(x)fitfunm(x, client_n, population, server_folder, neutral_params);
fitfunc=@(x)fitnessfun(x,w,net);

% NSGA-II parameters
optGA = gaoptimset(@gamultiobj);
optGA.Display = 'iter';
optGA.Generations = generations;
optGA.PopulationType = 'bitstring'; 
optGA.OutputFcns = @outfun;
optGA.ParetoFraction = 1;
optGA.CrossoverFcn=@crossoverscattered;
optGA.DistanceMeasureFcn = {@distancecrowding,'phenotype'};
optGA.PopulationSize = population;
optGA.Vectorized = 'on';
optGA.TolFun=1e-100;
save('optGA.mat','optGA')

% warning off;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Set profiler parameters
ga_start=tic;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Execute the NSGA-II
[Xga,Fga,~,output,~] = gamultiobj(fitfunc,nodes,[],[],[],[],[],[],optGA);
ga_all=toc(ga_start);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% [x,fval,exitflag,output,population,scores] = gamultiobj(fitfunc,nvars,A,b,Aeq,beq,[],[],optGA);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Format and save the output struct
filename = 'outresults';
load('all_solutions.mat');
load('states.mat');
all_solutions.Xga=Xga;
all_solutions.Fga=Fga;
all_solutions.output=output;
all_solutions.optGA=optGA;
all_solutions.times.ga_all=ga_all;
all_solutions.states=states;
all_solutions.target.network=net;
all_solutions.target.w=w;
save('all_solutions.mat', 'all_solutions');
movefile('all_solutions.mat',[filename '_' num2str(work_item) '.mat'])

delete('states.mat')
delete('optGA.mat')

diary off
