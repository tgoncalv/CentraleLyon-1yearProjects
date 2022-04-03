function [J] = M1(I)
% First morphological mask
% We set all pixels to 1 when the border pixels on the left and on the
% right are valued by 1
[H,W]=size(I);    
for x=1:H % The image is scanned line by line
    for y_left=1:W
        for y_right=y_left:W
            if (I(x,y_left)==1 && I(x,y_right)==1) % Checks if the border pixels are valued by 1
                for y=y_left:y_right % If that so, set all pixels between y_left and y_right to 1
                    I(x,y)=1;
                end
            end
        end
    end
end
J=I; 
end


