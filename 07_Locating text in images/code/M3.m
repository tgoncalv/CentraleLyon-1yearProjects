function [J] = M3(I)
% Third morphological mask
% Diagonal closure when two border pixels on the diagonal are valued by 1

J = bwmorph(I,'diag'); % The code already exists using bwmorph

end

