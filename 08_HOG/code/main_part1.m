close all;

I = imread('Images_HOG_1/car1.bmp');

[G, alpha_signed] = compute_gradient(I,'plot','signed');

plot_orientation(alpha_signed);

I_divided = divide_cells(alpha_signed,'dialog','plot');

histograms = HOG_features(I,'plot');