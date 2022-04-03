function [G,alpha_] = compute_gradient(I,plot,signed)
%COMPUTE_GRADIENT Computes the magnitude of the gradient and the
%orientation of the image I
if nargin<3
    signed = 'signed'; % Sets the default value of the 'plot' parameter
end

if nargin<2
    plot = 'no plot'; % Sets the default value of the 'plot' parameter
end

Dx = [-1 0 1];
Dy = [-1 0 1]';
Ix = conv2(I,Dx,'same');
Iy = conv2(I,Dy,'same');

G = (Ix.^2+Iy.^2).^0.5;
theta = atan2(Iy,Ix);

alpha = theta*180/pi;
alpha_ = zeros(size(alpha));
[nrows,ncols] = size(alpha_);
for i=1:nrows*ncols
    if alpha(i) >= 0
        alpha_(i) = alpha(i);
    else
        if strcmp(signed,'signed')
            alpha_(i) = alpha(i)+360;
        else
            alpha_(i) = alpha(i)+180;
        end
    end
end

%% Plot
if strcmp(plot,'plot')
    figure;
    sgtitle("Computation of the gradient of the image I");
    nrows = 2;
    ncols = 2;
    subplot(nrows,ncols,1); imshow(I); title("1. I = Original image");
    subplot(nrows,ncols,2); imshow(G,[0 255]); title("1. G = Magnitude of the gradient");
    subplot(nrows,ncols,3); imshow(Ix,[-255 0]); title("1. Ix = X-derivative");
    subplot(nrows,ncols,4); imshow(Iy,[-255 0]); title("1. Iy = Y-derivative");
end
end

