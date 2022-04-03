function [J] = M4(I)
% Fourth morphological mask
% We set all pixels to 1 when the border pixels on the left and on the
% right are valued by 1
[H,W]=size(I);    
for x=1:H % The image is scanned line by line
    for y_left=1:ceil(W*0.25)
        for y_right=floor(W*0.75+y_left):W % Reduces the number of iteration because the length of the segment needs to be greater than .75*W
            if (I(x,y_left)==1 && I(x,y_right)==1) % Checks if the border pixels are valued by 1
                for y=y_left:y_right % If that so, set all pixels between y_left and y_right to 1
                    I(x,y)=0;
                end
            end
        end
    end
end
J=I; 
end


