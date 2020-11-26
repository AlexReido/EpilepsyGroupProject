%CALLOPTIMISATION Calls the function for the optimisation of the epileptic
%model.
%
%   CALLOPTIMISATION() Calls the function that optimises the 
%   epileptic model. Finds the nodes that have to be removed in order to 
%   make the network stable (i.e. without epileptic attacks).
%
% Syntax:  calloptimisation()
%
% Inputs:
%    none
%
% Outputs: 
%    none
%
% Example:
%    calloptimisation()
%    This example starts a NSGA-II optimisation run.
%
% @author: Petroula Laiou, Eleftherios Avramidis $
% @email: P.Laiou@exeter.ac.uk el.avramidis@gmail.com $
% @date: 05/12/2017 $
% @version: 1.0 $
% Copyright: Not specified
function calloptimisation(work_item, generations, population)
%% Main arguments
% generations = 100;
% population = 200;
% work_item = 1;



%% Call optimisation function
optimrun(generations, population, work_item, net, w_ref)

end
