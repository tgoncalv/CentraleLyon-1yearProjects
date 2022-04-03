function [J] = M5(I)
% Fifth morphological mask

I = imcomplement(I);
I = bwmorph(I,'fill'); % The mask already exists in matlab
J = imcomplement(I);

end


