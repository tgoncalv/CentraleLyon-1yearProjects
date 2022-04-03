function [Rh] = representative_line(I,textRegion,L)
% Gets the representative horizontal line for specific text region
% The result is an array containing the coordinates of the left border and
% the right border of the line
top_line = textRegion(1);
bot_line = textRegion(2);
left_col = textRegion(3);
right_col = textRegion(4);

% I_extract = I(top_line:bot_line,left_col:right_col);
line_max = top_line;
count_max = 0;
for line=top_line:bot_line
    count = sum(I(line,left_col:right_col)==L);
    if count >= count_max
        line_max = line;
        count_max = count;
    end
end
Rh = [line_max left_col right_col];
end

