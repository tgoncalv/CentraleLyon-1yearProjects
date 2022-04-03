function [J] = M2(I)
% Second morphological mask
% Diagonal closure when two border piwels on the diagonal are valued by 1
[H,W]=size(I);    
for x = 1:H-1 % The image is scanned line by line
    for y_top=1:W
        for y_bot=1:W
            if (I(x,y_top)==1 && I(x+1,y_bot)==1) % Checks if the two borders pixels on the diagonal are valued by 1
                y_left = min(y_top,y_bot);
                y_right = max(y_top,y_bot);
                for y=y_left:y_right % If that so, set all pixels between them to 1
                    I(x,y)=1;
                    I(x+1,y)=1;
                end
            end
        end
    end
end
J=I; 

end

