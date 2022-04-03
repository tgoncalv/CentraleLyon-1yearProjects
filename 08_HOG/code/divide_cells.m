function I_divided = divide_cells(I,input,plot)
% Divide the image I into multiple cells
if nargin<3
    plot = 'no plot'; % Sets the default value of the 'plot' parameter
end

if nargin<2
    input = 'dialog'; % Sets the default value of the 'input' parameter
    % This parameter is used for HOG_features.m which already calls a
    % dialog box
end

if strcmp(plot,'plot')
    figure;
    imshow(I);
end

%% Dialog box
if strcmp(input,'dialog')
    prompt = {'Enter cell width:','Enter cell height:'};
    dlgtitle = 'Input';
    dims = [1 35];
    definput = {'20','20'};
    input = inputdlg(prompt,dlgtitle,dims,definput);
    width = str2num(input{1});
    height = str2num(input{2});
else
    width = input{1};
    height = input{2};
end




%% Creation of a cell object containing the divided image
[max_height,max_width] = size(I);
n_rows = ceil(max_height/height);
n_cols = ceil(max_width/width);
I_divided = cell(n_rows,n_cols);
for i=1:n_rows
    for j=1:n_cols
        if i==n_rows && j==n_cols
            I_divided{i,j} = I((i-1)*height+1:max_height , (j-1)*width+1:max_width);
        elseif i==n_rows
            I_divided{i,j} = I((i-1)*height+1:max_height , (j-1)*width+1:j*width);
        elseif j==n_cols
            I_divided{i,j} = I((i-1)*height+1:i*height , (j-1)*width+1:max_width);
          
        else
            I_divided{i,j} = I((i-1)*height+1:i*height , (j-1)*width+1:j*width);
        end
        
    end
end
    
%% Plots the result if asked to do so
if strcmp(plot,'plot')
    I_plot = cat(3,I,I,I);
    for i=1:floor(max_height/height)
        I_plot(i*height,:,1)=255;
        I_plot(i*height,:,2)=0;
        I_plot(i*height,:,3)=0;
    end
    for i=1:floor(max_width/width)
        I_plot(:,i*width,1)=255;
        I_plot(:,i*width,2)=0;
        I_plot(:,i*width,3)=0;
    end
    title('Divide I into cells');
    imshow(I_plot);
end
end

