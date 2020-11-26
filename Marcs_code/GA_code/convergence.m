function convergence(folderslist, folderidlist)
%CALLCONVERGENCE Calls the function for the plotting of the convergence
%metrics.
%
%   CALLCONVERGENCE() Calls the function that optimises the
%   epileptic model. Finds the nodes that have to be removed in order to
%   make the network stable (i.e. without epileptic attacks).
%
% Syntax:  callconvergence(folderslist, folderidlist)
%
% Inputs:
%    folderslist        - Cell list with the results folder names. Each 
%                         folder must include runs with one combination of 
%                         NSGA-II parameter values.
%    folderidlist       - Cell list with the results folder ids.
%
% Outputs:
%    none
%
% Example:
%    callconvergence({'pop_40', 'pop_80'}, {'pop 40','pop 80'})
%    This example plots the convergence metrics.
%
% Other m-files required: none
% Subfunctions: getMaxScorePerObjective, HypervolumeCH, my_euclid
% MAT-files required: none
%
% See also: E. Avramidis & O.E. Akman. Optimisation of an exemplar oculomotor model
% using multi-objective genetic algorithms executed on a GPU-CPU combination.
% BMC Syst. Biol., 11: 40 (2017)
%
% @author: Eleftherios Avramidis $
% @email: el.avramidis@gmail.com $
% @date: 10/12/2017 $
% @version: 1.0 $
% Copyright: Not specified

%% Support variables

callpath = pwd;

% Number of NSGA-II parameter combinations
numparamsets = length(folderslist);
if numparamsets~=length(folderidlist)
    error('folderslist and folderidlist must have the same number of cells!')
end

% Check that all folders in folderslist have the same number of result
% files
for i=1:numparamsets
    eval(['cd ' char(folderslist(i))]);
    
    fs = dir('*.mat');
    numfiles(i) = numel(fs);
    
    load('outresults_1.mat')
    gens = all_solutions.output.generations;
    
    eval(['cd ' callpath])
end
if length(numfiles(numfiles==numfiles(1)))~=numparamsets
    error('Each folder must have the same number of results files!')
end

%% Set the number of results files in each folder and the number of generations
numruns = numfiles(1);

%% Calculate maximum score per objective and generations number
count=1;
r=[0 0];
for i=1:numparamsets
    eval(['cd ' char(folderslist(i))]);
    
    for the_run=1:numruns
        load(['outresults_' num2str(the_run) '.mat']);
        
        check_gens(count) = all_solutions.output.generations;
        count = count + 1;
        
        %         r=[0 0];
        for gen=1
            ind=find(all_solutions.states(1, gen).Rank==1);
            Scores=all_solutions.states(1, gen).Score(ind,:);
            
            m = getMaxScorePerObjective(Scores);
        end
        
        for j=1:2
            if m(j)>r(j)
                r(j)=m(j);
            end
        end
    end
    eval(['cd ' callpath])
end

if length(check_gens(check_gens==check_gens(1)))~=(count-1)
    error('Each results file must have the same number of generations!')
end

%% Calculate the mean and std hypervolume and Euclidian distance
for i=1:numparamsets
    eval(['cd ' char(folderslist(i))]);
    
    for the_run=1:numruns
        load(['outresults_' num2str(the_run) '.mat']);
        
        for gen=1:gens
            if gen<=length(all_solutions.states)
                ind=find(all_solutions.states(1, gen).Rank==1);
                
                Scores=all_solutions.states(1, gen).Score(ind,:);
            end
            v(i,the_run,gen)=HypervolumeCH(Scores,r);
            
            origin=zeros(size(Scores));
            
            d(i,the_run,gen) = min(my_euclid(origin,Scores));
            % d(k,the_run,gen) = min(Scores(:,1));
        end
        
        for gen=2:gens
            if v(i,the_run,gen-1)==0
                v2(i,the_run,gen)=0;
            else
                v2(i,the_run,gen)=(v(i,the_run,gen)-v(i,the_run,gen-1))*100/v(i,the_run,gen-1);
            end
            
            if d(i,the_run,gen-1)==0
                d2(i,the_run,gen)=0;
            else
                d2(i,the_run,gen)=(d(i,the_run,gen)-d(i,the_run,gen-1))*100/d(i,the_run,gen-1);
            end
        end
    end
    eval(['cd ' callpath])
end

for i=1:numparamsets
    subplot(1,4,1)
    plot(mean(1-squeeze(v(i,:,:))))
    hold on
    ylabel('Mean hypervolume metric')
    xlabel('Generation number')
    subplot(1,4,2)
    hold on
    plot(mean(squeeze(d(i,:,:))))
    ylabel('Mean Eucledean distance from origin axis')
    xlabel('Generation number')
end

for i=1:numparamsets
    subplot(1,4,3)
    plot(std(1-squeeze(v(i,:,:))))
    hold on
    ylabel('STD hypervolume metric')
    xlabel('Generation number')
    subplot(1,4,4)
    plot(std(squeeze(d(i,:,:))))
    hold on
    ylabel('STD Eucledean distance from origin axis')
    xlabel('Generation number')
end
legend(folderidlist)

%% Resize the plot
% [left bottom width height]
lastpos=get(gcf,'Position');
lastpos(3)=lastpos(3)*2;
set(gcf,'Position',lastpos);

end

function m = getMaxScorePerObjective(scores)
%GETMAXSCOREPEROBJECTIVE Calculates and returns the maximum value for each 
%objective for a number of individuals.
%
%   GETMAXSCOREPEROBJECTIVE(scores) Calculates and returns the maximum
%   value for each objective for a number of individuals.
%
% Syntax:  getMaxScorePerObjective(scores)
%
% Inputs:
%    scores        - Matrix with the scores for each objective for a number
%                    of individuals.
%
% Outputs:
%    m             - Maximum score for each objective.
%
% Example:
%    m = getMaxScorePerObjective([1,2,3,4;3,1,4,6])
%    This example returns the maximum value of each objective and stores it
%    in the return variable m.
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%
% See also: E. Avramidis & O.E. Akman. Optimisation of an exemplar oculomotor model
% using multi-objective genetic algorithms executed on a GPU-CPU combination.
% BMC Syst. Biol., 11: 40 (2017)
%
% @author: Eleftherios Avramidis $
% @email: el.avramidis@gmail.com $
% @date: 10/12/2017 $
% @version: 1.0 $
% Copyright: Not specified

[~, c]=size(scores);
m = zeros(c,1);
for i=1:c
    m(i)=max(scores(:,i));
end

end

function v=HypervolumeCH(Scores, r)
%HYPERVOLUMECH Calculates the hypervolume metric for a pareto fron and a point.
%
%   HYPERVOLUMECH(scores ,r) Calculates the hypervolume metric for a pareto
%   front and point r.
%
% Syntax:  v=HypervolumeCH(Scores, r)
%
% Inputs:
%    Scores        - Parero front
%    r             - Point for the calculation of the hypervolume against
%                    the Pareto front Score.
%
% Outputs:
%    v             - Hypervolume.
%
% Example:
%    v = HypervolumeCH([1,2,3,4;3,1,4,6], [4,5])
%    This example calculates the Pareto front [1,2,3,4;3,1,4,6] against the
%    point [4,5].
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%
% See also: E. Avramidis & O.E. Akman. Optimisation of an exemplar oculomotor model
% using multi-objective genetic algorithms executed on a GPU-CPU combination.
% BMC Syst. Biol., 11: 40 (2017)
%
% @author: Eleftherios Avramidis $
% @email: el.avramidis@gmail.com $
% @date: 10/12/2017 $
% @version: 1.0 $
% Copyright: Not specified

ind=find(Scores(:,1)>r(1));
Scores(ind,:)=[];
ind=find(Scores(:,2)>r(2));
Scores(ind,:)=[];

Scores=[Scores; r];

r2=[r(1) min(Scores(:,2))];
r3=[min(Scores(:,1)) r(2)];
Scores=[Scores; r2];
Scores=[Scores; r3];

x = Scores(:,1);
y = Scores(:,2);
% [x,y] = pol2cart(xx,yy);
[k, v] = convhull(x,y);
% plot(x(k),y(k),'r-',x,y,'b*')

vbox=r(1)*r(2);
v=v/vbox;
end

function d = my_euclid(origin, A)
%MY_EUCLID Calculates the Euclidean distance between the points in two
%vectors.
%
%   MY_EUCLID(origin, A) Calculates the Euclidean distance between the
%   points of the vectors origin and A.
%
% Syntax:  d = my_euclid( origin, A )
%
% Inputs:
%    origin        - First vector.
%    A             - Second vector.
%
% Outputs:
%    d             - Vector with the distances for each line of the
%                    vectors.
%
% Example:
%    d = my_euclid([1,2,3,4], [3,1,4,6])
%    This example calculates the distance between the vectors [1,2,3,4] and
%    [3,1,4,6].
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%
% See also: E. Avramidis & O.E. Akman. Optimisation of an exemplar oculomotor model
% using multi-objective genetic algorithms executed on a GPU-CPU combination.
% BMC Syst. Biol., 11: 40 (2017)
%
% @author: Eleftherios Avramidis $
% @email: el.avramidis@gmail.com $
% @date: 10/12/2017 $
% @version: 1.0 $
% Copyright: Not specified

% This works for 2D. TODO: Make it work for 3D
d=sqrt(((origin(:,1)-A(:,1)).^2)+((origin(:,2)-A(:,2)).^2));

end