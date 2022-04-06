close all;
%run('C:\Users\taiga\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\vlfeat-0.9.21\toolbox\vl_setup.m')

%% Parameters
                     
% First step: compute the SIFT values
resize_param = 1; % The images where Charlie is hidden will be resized by this value
resize_param_head = 0.8; % The image of the head of Charlie (sample image) will be resized
gauss_filt = 0.5; % All the images will be filtered by the gaussian filter with the std value precised here
compute_sift = false; % The SIFT's computation may take some time. The data will thus be
                     % initialized only once and stored in the variables list so that the code
                     % can be modified without needing to run SIFT computation again.
                     
% Second step: draw cercles where Charlie may be there
match_threshold = 1; % Threshold of vl_ubcmatch. We find charlie with the following values for each images:
                     % I1: too small  -  I2: 1.4  -  I3: 1  -  I4: 1.62  -  I5: 1.48
compute_ubcmatch = false; % Compute the values only if the parameters above have been updated
plot_secondStep = "I4"; % Enter the image to plot. The plot corresponds to the result of 1st and 2nd steps.

% Third step: Try another matching by slicing the sample image
slicing = [80 115 25 80]; % Troncate the image with: [xmin xmax ymin ymax]
                           %I2 : 80 115 25 80
                           %I3 : no
                           %I4 : 80 115 25 80    
                           %I5 : 80 115 25 100
compute_ubcmatch_thirdstep = true;
plot_thirdStep = "I4"; % Enter the image to plot.


%% First step: Compute SIFT
                     
if(compute_sift)
    sample = imread('Charlie.jpg');
    I1 = imread('Charlie1.jpg');
    I2 = imread('Charlie2.jpg');
    I3 = imread('Charlie3.jpg');
    I4 = imread('Charlie4.jpg');
    I5 = imread('Charlie5.jpg');
    
    charlie_head = sample(1:180,180:320,:);
    I = charlie_head; % Extracting the head of Charlie Use I for every images so that no useless variables are created
    I = im2single(I);
    I = rgb2gray(I);
    I = imresize(I,resize_param_head);
    I = imgaussfilt(I,0.5);
    [f,d] = vl_sift(I);
    
    I = I1; % Use I for every images so that no useless variables are created
    I = im2single(I);
    I = rgb2gray(I);
    I = imresize(I,resize_param);
    I = imgaussfilt(I,gauss_filt);
    [f1,d1] = vl_sift(I);

    I = I2; % Use I for every images so that no useless variables are created
    I = im2single(I);
    I = rgb2gray(I);
    I = imresize(I,resize_param);
    I = imgaussfilt(I,gauss_filt);
    [f2,d2] = vl_sift(I);
    
    I = I3; % Use I for every images so that no useless variables are created
    I = im2single(I);
    I = rgb2gray(I);
    I = imresize(I,resize_param);
    I = imgaussfilt(I,gauss_filt);
    [f3,d3] = vl_sift(I);
    
    I = I4; % Use I for every images so that no useless variables are created
    I = im2single(I);
    I = rgb2gray(I);
    I = imresize(I,resize_param);
    I = imgaussfilt(I,gauss_filt);
    [f4,d4] = vl_sift(I);
    
    I = I5; % Use I for every images so that no useless variables are created
    I = im2single(I);
    I = rgb2gray(I);
    I = imresize(I,resize_param);
    I = imgaussfilt(I,gauss_filt);
    [f5,d5] = vl_sift(I);
end

%% Second step: Match SIFT values

if(compute_ubcmatch)
    [matches, scores] = vl_ubcmatch(d,d1,match_threshold); 
    [scores, sortIdx] = sort(scores,'descend');
    matches1 = matches(:,sortIdx);
    X1 = f1(1:2, matches1(2,:))';
    r1 = f1(3, matches1(2,:))';
    
    [matches, scores] = vl_ubcmatch(d,d2,match_threshold); 
    [scores, sortIdx] = sort(scores,'descend');
    matches2 = matches(:,sortIdx);
    X2 = f2(1:2, matches2(2,:))';
    r2 = f2(3, matches2(2,:))';
    
    [matches, scores] = vl_ubcmatch(d,d3,match_threshold); 
    [scores, sortIdx] = sort(scores,'descend');
    matches3 = matches(:,sortIdx);
    X3 = f3(1:2, matches3(2,:))';
    r3 = f3(3, matches3(2,:))';
    
    [matches, scores] = vl_ubcmatch(d,d4,match_threshold); 
    [scores, sortIdx] = sort(scores,'descend');
    matches4 = matches(:,sortIdx);
    X4 = f4(1:2, matches4(2,:))';
    r4 = f4(3, matches4(2,:))';
    
    [matches, scores] = vl_ubcmatch(d,d5,match_threshold); 
    [scores, sortIdx] = sort(scores,'descend');
    matches5 = matches(:,sortIdx);
    X5 = f5(1:2, matches5(2,:))';
    r5 = f5(3, matches5(2,:))';
end

if(plot_secondStep == "I1")
    figure;
    imshow(I1);
    viscircles(X1/resize_param, 50*r1,'color','magenta');
elseif(plot_secondStep == "I2")
    figure;
    imshow(I2);
    viscircles(X2/resize_param, 50*r2,'color','magenta');
elseif(plot_secondStep == "I3")
    figure;
    imshow(I3);
    viscircles(X3/resize_param, 50*r3,'color','magenta');
elseif(plot_secondStep == "I4")
    figure;
    imshow(I4);
    viscircles(X4/resize_param, 50*r4,'color','magenta');
elseif(plot_secondStep == "I5")
    figure;
    imshow(I5);
    viscircles(X5/resize_param, 50*r5,'color','magenta');
end


% figure;
% X = f(1:2, matches(1,:))';
% r = f(3, matches(1,:))';
% imshow(imresize(I,1/resize_param_head));
% viscircles(f(1:2,:)'/resize_param_head,f(3,:)','color','magenta');

%% Third step: Try another matching by slicing the sample image

if(compute_ubcmatch_thirdstep)
    xmin = slicing(1);
    xmax = slicing(2);
    ymin = slicing(3);
    ymax = slicing(4);
    charlie_head_up = charlie_head(xmin:xmax,ymin:ymax,:);
    I = charlie_head_up;
    I = im2single(I);
    I = rgb2gray(I);
    I = imresize(I,resize_param_head);
    I = imgaussfilt(I,gauss_filt);
    [f_up,d_up] = vl_sift(I);

    f1_up = f1(:, matches1(2,:));
    d1_up = d1(:, matches1(2,:));
    [matches_up, scores_up] = vl_ubcmatch(d_up,d1_up,1);
    [scores, sortIdx] = sort(scores_up,'descend');
    matches_up = matches_up(:,sortIdx);
    X1_up = f1_up(1:2, matches_up(2,1))'; % We only conserve the feature with the best score
    r1_up = f1_up(3, matches_up(2,1))';

    f2_up = f2(:, matches2(2,:));
    d2_up = d2(:, matches2(2,:));
    [matches_up, scores_up] = vl_ubcmatch(d_up,d2_up,1);
    [scores, sortIdx] = sort(scores_up,'descend');
    matches_up = matches_up(:,sortIdx);
    X2_up = f2_up(1:2, matches_up(2,1))'; % We only conserve the feature with the best score
    r2_up = f2_up(3, matches_up(2,1))';

    f3_up = f3(:, matches3(2,:));
    d3_up = d3(:, matches3(2,:));
    [matches_up, scores_up] = vl_ubcmatch(d_up,d3_up,1);
    [scores, sortIdx] = sort(scores_up,'descend');
    matches_up = matches_up(:,sortIdx);
    X3_up = f3_up(1:2, matches_up(2,:))'; % We only conserve the feature with the best score
    r3_up = f3_up(3, matches_up(2,:))';

    f4_up = f4(:, matches4(2,:));
    d4_up = d4(:, matches4(2,:));
    [matches_up, scores_up] = vl_ubcmatch(d_up,d4_up,1);
    [scores, sortIdx] = sort(scores_up,'descend');
    matches_up = matches_up(:,sortIdx);
    X4_up = f4_up(1:2, matches_up(2,1))'; % We only conserve the feature with the best score
    r4_up = f4_up(3, matches_up(2,1))';

    f5_up = f5(:, matches5(2,:));
    d5_up = d5(:, matches5(2,:));
    [matches_up, scores_up] = vl_ubcmatch(d_up,d5_up,1);
    [scores, sortIdx] = sort(scores_up,'descend');
    matches_up = matches_up(:,sortIdx);
    X5_up = f5_up(1:2, matches_up(2,1))'; % We only conserve the feature with the best score
    r5_up = f5_up(3, matches_up(2,1))';
end

if(plot_thirdStep == "I1")
    figure;
    imshow(I1);
    viscircles(X1_up/resize_param, 50*r1_up,'color','magenta');
elseif(plot_thirdStep == "I2")
    figure;
    imshow(I2);
    viscircles(X2_up/resize_param, 50*r2_up,'color','magenta');
elseif(plot_thirdStep == "I3")
    figure;
    imshow(I3);
    viscircles(X3_up/resize_param, 50*r3_up,'color','magenta');
elseif(plot_thirdStep == "I4")
    figure;
    imshow(I4);
    viscircles(X4_up/resize_param, 50*r4_up,'color','magenta');
elseif(plot_thirdStep == "I5")
    figure;
    imshow(I5);
    viscircles(X5_up/resize_param, 50*r5_up,'color','magenta');
end





