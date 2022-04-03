function [] = plot_orientation(alpha_signed)
% Represents all the pixels having the gradient orientation in the interval
% [0 180] with yellow and all gradients in the interval [180 360] with blue

plot = ones(size(alpha_signed));

[nrows,ncols] = size(alpha_signed);
for i=1:nrows*ncols
    if (0 <= alpha_signed(i) && alpha_signed(i) <= 180)
        plot(i) = 2;
    end
end

figure;
colormap = [0 0 1 ; 1 1 0];
imshow(plot,colormap);

end

