function [p_x] = probability(X, new_example)
  % Function finds the probability of a new example
  % to determine if it's an anomaly or not
  
  %Initialize variables
  [m,n] = size(X);
  mu = zeros(n,1);
  sigma_squared = zeros(n,1);  

  %calculate parameters
  mu = sum(X)/m 
  sigma_squared = (1/m)*(sum((X-u).^2))
  
  p_x = pi/(sqrt(2*pi*
  
endfunction
