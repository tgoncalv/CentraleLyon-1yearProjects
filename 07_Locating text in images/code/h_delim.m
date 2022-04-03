function [x_top,x_bot] = h_delim(H,Rh,L)
% Gets the top and bottom lines which delimite text region
y_left = Rh(2);
y_right = Rh(3);
[Hh,Wh] = size(H);

x = Rh(1);
x_top = 0;
while(x_top == 0)
    if x == 1
        x_top = x;
    else
        for y=y_left:y_right
            if (H(x,y)==L && H(x-1,y)==L)
                x = x - 1;
                break
            elseif y==y_right
                x_top = x;
            end
        end
    end
end  

x = Rh(1);
x_bot = 0;
while(x_bot == 0)
    if x == Hh
        x_bot = x;
    else
        for y=y_left:y_right
            if (H(x,y)==L && H(x+1,y)==L)
                x = x + 1;
                break
            elseif y==y_right
                x_bot = x;
            end
        end
    end
end
end