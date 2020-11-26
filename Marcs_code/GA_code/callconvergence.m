%CALLCONVERGENCE Calls the function for the plotting of the convergence
%metrics.
%
%   CALLCONVERGENCE() Calls the function for the plotting of the convergence
%   metrics.
%
% Syntax:  callconvergence()
%
% Inputs:
%    none
%
% Outputs: 
%    none
%
% Example:
%    callconvergence()
%    This example plots the convergence metrics.
%
% Other m-files required: convergence.m
% Subfunctions: none
% MAT-files required: none
%
% See also: E. Avramidis & O.E. Akman. Optimisation of an exemplar oculomotor model
% using multi-objective genetic algorithms executed on a GPU-CPU combination.
% BMC Syst. Biol., 11: 40 (2017)
%
% @author: Petroula Laiou, Eleftherios Avramidis $
% @email: P.Laiou@exeter.ac.uk el.avramidis@gmail.com $
% @date: 05/12/2017 $
% @version: 1.0 $
% Copyright: Not specified

clear variables

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Main arguments

% Cell list with the results folder
%folderslist = {'exampleresults\pop_40', 'exampleresults\pop_80'};
folderslist = {'EDK_results'};
% Cell list with the results folder ids
folderidlist = {'pop 200'};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Call optimisation function
convergence(folderslist, folderidlist);

