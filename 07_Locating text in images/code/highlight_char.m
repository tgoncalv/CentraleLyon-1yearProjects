function [J] = highlight_char(I,u,L,fmin)
% Highlight character pixels from the background
% It consist of mapping each gray level a=0:L into a gray level v=u:L
% accorging to the transformation v=f(a). This function transforms the grey level of every
% pixels having a>u by L, otherwise the grey level value becomes equal to
% fmin (fmin = a or u)
[H,W]=size(I);    
for x=1:H % The image is scanned line by line
    for y=1:W
        if I(x,y) > u
            I(x,y) = L;
        else
            if fmin=="u"
                I(x,y) = u;
            end
        end
    end
end         
J = I;
end

