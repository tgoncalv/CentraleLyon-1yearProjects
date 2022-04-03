close all;

%% Question 1
I = imread('Images_HOG_2/hog_similar.bmp');

[height,width] = size(I);

coords_1 = [0 0 63 127] + ones(1,4); % Matlab coordinates start from 1
coords_2 = [90 0 153 127] + ones(1,4); % Matlab coordinates start from 1

n_bins = 12;
cell_width = 64;
cell_height = 128;

object1 = I(height-(coords_1(4)-coords_1(2)):height , coords_1(1):coords_1(3));
object2 = I(height-(coords_1(4)-coords_1(2)):height , coords_2(1):coords_2(3));

object1_HOG = HOG_features(object1,'no plot', cell_width, cell_height, n_bins);
object1_HOG = object1_HOG{1};
object2_HOG = HOG_features(object2,'no plot', cell_width, cell_height, n_bins);
object2_HOG = object2_HOG{1};

figure;
sgtitle('hog\_similar.bmp');
subplot(1,2,1); imshow(object1);
subplot(1,2,2); imshow(object2);

similarity_1 = cosine_similarity(object1_HOG,object2_HOG)

%% Question 2
I = imread('Images_HOG_2/hog_different.bmp');

[height,width] = size(I);

object1 = I(height-(coords_1(4)-coords_1(2)):height , coords_1(1):coords_1(3));
object2 = I(height-(coords_1(4)-coords_1(2)):height , coords_2(1):coords_2(3));

object1_HOG = HOG_features(object1,'no plot', cell_width, cell_height, n_bins);
object1_HOG = object1_HOG{1};
object2_HOG = HOG_features(object2,'no plot', cell_width, cell_height, n_bins);
object2_HOG = object2_HOG{1};

figure;
sgtitle('hog\_different.bmp');
subplot(1,2,1); imshow(object1);
subplot(1,2,2); imshow(object2);

similarity_2 = cosine_similarity(object1_HOG,object2_HOG)

%% Question 3
I = imread('Images_HOG_2/hog_similar.bmp');

[height,width] = size(I);

n_bins = 9;
cell_width = 16;
cell_height = 16;

object1 = I(height-(coords_1(4)-coords_1(2)):height , coords_1(1):coords_1(3));
object2 = I(height-(coords_1(4)-coords_1(2)):height , coords_2(1):coords_2(3));

object1_HOG_cells = HOG_features(object1,'no plot', cell_width, cell_height, n_bins);
object1_HOG = [];
[m,n] = size(object1_HOG_cells);
for i=1:m*n
    object1_HOG = [object1_HOG, object1_HOG_cells{i}];
end

object2_HOG_cells = HOG_features(object2,'no plot', cell_width, cell_height, n_bins);
object2_HOG = [];
[m,n] = size(object2_HOG_cells);
for i=1:m*n
    object2_HOG = [object2_HOG, object2_HOG_cells{i}];
end

similarity_1_version2 = cosine_similarity(object1_HOG,object2_HOG)

%% Question 4
I = imread('Images_HOG_2/hog_different.bmp');

[height,width] = size(I);

n_bins = 9;
cell_width = 16;
cell_height = 16;

object1 = I(height-(coords_1(4)-coords_1(2)):height , coords_1(1):coords_1(3));
object2 = I(height-(coords_1(4)-coords_1(2)):height , coords_2(1):coords_2(3));

object1_HOG_cells = HOG_features(object1,'no plot', cell_width, cell_height, n_bins);
object1_HOG = [];
[m,n] = size(object1_HOG_cells);
for i=1:m*n
    object1_HOG = [object1_HOG, object1_HOG_cells{i}];
end

object2_HOG_cells = HOG_features(object2,'no plot', cell_width, cell_height, n_bins);
object2_HOG = [];
[m,n] = size(object2_HOG_cells);
for i=1:m*n
    object2_HOG = [object2_HOG, object2_HOG_cells{i}];
end

similarity_2_version2 = cosine_similarity(object1_HOG,object2_HOG)












