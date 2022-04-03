clear all;
%% 1 Digital image transformation

% Read the image
I = imread('Images/1.jpg');

% Stage 1: Convert the colored image I into an image in grey level G
G =  rgb2gray(I);
[Gh,Gw] = size(G);

% Stage 2: Transpose G to make possible the detection of vertical texts
% G = G'

% Stage 3: If possible, define a sub-zone of the image in which text
% regions are going to be looked for
% Cannot be used here as the text can be located everywhere


%% 2 Enchancement of text region patterns
K = G;

% Multi-resolution method
M = 0.131; % Default value: 0.131
K = imresize(K, M, 'nearest');
K_resize = K; % Stores the image to plot it later

% Conversion of G into a binary image
threshold = 0.7; % Default value: 0.7
K = im2bw(K,threshold);
K_BW = K; % Stores the image to plot it later


%% 5.2 Negative form elimination : Fifth morphological mask
K = M5(K);
K = M4(K);
K_M4_M5 = K; % Stores the image to plot it later


%% 3 Potential text regions localization
[Kh,Kw]=size(K);
Kbis = im2bw(ones(Kh,Kw));
while norm(double(K-Kbis))> 0.01 % While the morphological mask does effecive changes to the image
    Kbis = K;
    K=M1(K);
    K=M3(K);
    K=M2(K);
end
K_M1_M2_M3 = K; % Stores the image to plot it later


%% 4.1 Background pixels separation
L = 255; % Represents the white colour
u = 255;
nb = sum(G(:)==u); % Number of pixels having the value 255
nb_tot = Gh*Gw;
u_threshold = 0.02; % Default value: 0.02
while(nb/nb_tot < u_threshold && u>0)
    u = u - 1;
    nb = nb + sum(G(:)==u);
end
H = highlight_char(G,u,L,'a');


%% 4.2 Effective text region filtering
regions_labels = bwlabel(imresize(K,size(G)),8); % Creates labels to distinguish each regions
n_regions = max(regions_labels(:)); % Total number of regions
regions_coor = zeros(n_regions,4); % Coordinates of the regions (the regions are supposed to be rectangular)
for i=1:n_regions
    [rows,cols] = find(regions_labels==i);
    rtop = min(rows);
    rbot = max(rows);
    cleft = min(cols);
    cright = max(cols);
    new_region = [rtop rbot cleft cright];
    regions_coor(i,:) = new_region;
end

regions = [];
regions_labels_2 = regions_labels;
for i=1:size(regions_coor,1)
    rect = regions_coor(i,:);
    extract_H = H(rect(1):rect(2),rect(3):rect(4));
    count = imhist(extract_H);
    [max1,P1] = max(count); % Highest value in the histogram of the region
    count = count([1:P1-1 P1+1:end]); % Remove the maximum value
    [max2,P2] = max(count); % Second highest value in the histogram of the region
    
%     subplot(2,2,i); imhist(extract_H);
    
    D_P1_P2 = abs(P2-P1);
    tot_bin_nb = sum(imhist(H)>0); % Total bin number in the gray scale levels
    D_threshold = 0.35; % Default value: 0.35
    if (D_P1_P2 > D_threshold*tot_bin_nb)
        regions = [regions ; rect]; % The region has an effective text
    else
        regions_labels_2(regions_labels_2==i)=0; % Deletes the region because it doesn't have any texts
    end
end


%% 5.1 Delimitation of text region boundaries
imresult = I;
for i=1:size(regions,1)
    Rh = representative_line(H,regions(i,:),L);
    [x_top,x_bot] = h_delim(H,Rh,L);
    [y_left,y_right] = v_delim(H,Rh,L);
    for x=x_top:x_bot
        imresult(x,y_left,:)=[255 255 255];
        imresult(x,y_right,:)=[255 255 255];
    end
    for y=y_left:y_right
        imresult(x_top,y,:)=[255 255 255];
        imresult(x_bot,y,:)=[255 255 255];
    end
end


%% Show result
figure;
sgtitle("Figures for the parts 1,2,3 and 5");
nrows = 2;
ncols = 3;
subplot(nrows,ncols,1); imshow(I); title("1. I = Original image");
subplot(nrows,ncols,2); imshow(G); title ("2. G = rgb2gray");
subplot(nrows,ncols,3); imshow(K_resize); title("4. K = imresize");
subplot(nrows,ncols,4); imshow(K_BW); title("3. K = imbinarize");
subplot(nrows,ncols,5); imshow(K_M4_M5); title("5. K = M4+M5(K)");
subplot(nrows,ncols,6); imshow(K_M1_M2_M3); title("6. K = M1+M2+M3(K)");

figure;
sgtitle("Figures for the parts 1 and 4");
nrows = 3;
ncols = 3;
subplot(nrows,ncols,1); imshow(I); title("1. I = Original image");
subplot(nrows,ncols,2); imshow(G); title ("2. G = rgb2gray");
subplot(nrows,ncols,3); imshow(H); title ("3. H = highlight char");
subplot(nrows,ncols,4); imshow(regions_labels); title ("4 potential regions");
subplot(nrows,ncols,5); imshow(regions_labels_2); title ("5 effective regions");

figure;
sgtitle("Result");
nrows=1;
ncols=2;
subplot(nrows,ncols,1); imshow(imresult); title("text regions delimiters");
subplot(nrows,ncols,2); imshow(regions_labels_2); title("text regions");