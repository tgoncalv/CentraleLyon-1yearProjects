function [y_left,y_right] = v_delim(H,Rh,L)
% Gets the left and right borders which delimite text region
x = Rh(1);
[Hh,Wh] = size(H);

y = Rh(2);
yr = Rh(3);
y_left = 0;
while(y_left == 0)
    if (y==1 || yr-y == floor(Wh*0.75))
        y_left = y;
    elseif H(x,y)==H(x,y-1)
        y = y - 1;
    else
        y_left = y;
    end
end  

yl = Rh(2);
y = Rh(3);
y_right = 0;
while(y_right == 0)
    if (y==Wh || y-yl == floor(Wh*0.75))
        y_right = y;
    elseif H(x,y)==H(x,y+1)
        y = y + 1;
    else
        y_right = y;
    end
end  

end