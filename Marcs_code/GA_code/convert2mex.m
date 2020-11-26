%   CONVERT2MEX() Generate a mex file for the theta_model_P function using
%   MATLAB Coder.
%
% Syntax:  convert2mex()
%
% Inputs:
%    none
%
% Outputs: 
%    none
%
% Example:
%    convert2mex()
%    This example Generate a mex file for the theta_model_P function using
%    MATLAB Coder.
%
% Other m-files required: theta_model_P.m
% Subfunctions: none
% MAT-files required: none
%
% See also: Goodfellow, M., Rummel, C., Abela, E., Richardson, M. P., 
% Schindler, K., & Terry, J. R. (2016). Estimation of brain network 
% ictogenicity predicts outcome from epilepsy surgery. Scientific Reports, 
% 6(1), 29215. https://doi.org/10.1038/srep29215
%
% @author: Petroula Laiou $
% @email: P.Laiou@exeter.ac.uk $
% @date: 05/12/2017 $
% @version: 1.0 $
% Copyright: Not specified

clear variables

network=coder.typeof(ones(130,130), [], 1); % I placed 130 because my nets were had at most 130 nodes 
w =  coder.typeof(1); % just a double
nodes_resected =  coder.typeof(1); % just a double

codegen theta_model_P.m -args {network, w, nodes_resected}

