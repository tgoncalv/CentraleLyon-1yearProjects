clear all
%% First morphological mask
T = [1 0 0 0 0 0 1 0];
T = reshape(T,[2,4]);
BW1 = imbinarize(T);
M1_res = M1(BW1);


%% Second morphological mask
T = [0 1 0 0 1 0];
T = reshape(T,[2,3]);
BW2 = imbinarize(T);
M2_res = M2(BW2);

%% Third morphological mask
T = [0 1 0 0 0 1 1 0 0 0 1 0 0 0 0 0 0 0];
T = reshape(T,[6,3]);
BW3 = imbinarize(T);
M3_res = M3(BW3);

%% Fourth morphological mask
T = [1 1 0 0 0 0 0 0 0 0 1 0 0 0];
BW4 = imbinarize(T)
M4_res = M4(BW4)

%% Fifth morphological mask
T = [0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 0 1 0 1 1 1 1];
T = reshape(T,[4,7]);
BW5 = imbinarize(T);
M5_res = M5(BW5);