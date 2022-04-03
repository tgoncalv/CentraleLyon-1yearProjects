function [histograms] = HOG_features(I,plot, width, height, n_bins)
% Computes the HOG features for a given image I
if nargin<3
    dialogbox = "dialogbox";
else
    dialogbox = "none";
end

if nargin<2
    plot = 'no plot'; % Sets the default value of the 'plot' parameter
end

%% Dialog box
if strcmp(dialogbox,'dialogbox')
    prompt = {'Enter cell width:','Enter cell height:','Enter the number of bins'};
    dlgtitle = 'Input';
    dims = [1 35];
    definput = {'30','30','9'};

    input = inputdlg(prompt,dlgtitle,dims,definput);
    width = str2num(input{1});
    height = str2num(input{2});
    n_bins = str2num(input{3});
end
    
%% Divide the image into cells using divide_cells.m
[G, alpha_signed] = compute_gradient(I,'no plot','signed');
G_divided = divide_cells(G,{width,height},'no plot');
alpha_divided = divide_cells(alpha_signed,{width,height},'no plot');
[n_rows, n_cols] = size(G_divided);

%% Histogram computation
edges = 0: 360/n_bins : 360;
histograms = cell(n_rows,n_cols);
for i=1:n_rows
    for j=1:n_cols
        alpha = alpha_divided{i,j};
        hist = zeros(1,n_bins);
        for n=1:n_bins
            if n==n_bins
                count = (edges(n)<= alpha)&(alpha <= edges(n+1)).*G_divided{i,j}.^0.5;
            else
                count = (edges(n)<= alpha)&(alpha < edges(n+1)).*G_divided{i,j}.^0.5;
            end
            hist(n) = sum(count,'all');
        end
        histograms{i,j} = hist;
    end
end

%% Plot the histograms
if strcmp(plot,'plot')
    [max_height, max_width] = size(I);
    height = max_height/n_rows;
    width = max_width/n_cols;
    f = figure();
    pos = f.Position;
    f.Position = [pos(1) pos(2) max_width, max_height];
    for i=1:n_rows
        for j=1:n_cols
            pos = [width*(j-1)/max_width 1-height*(i)/(max_height) width/(max_width), height/(max_height)];
            subplot('Position',pos);
            histogram('BinEdges',edges,'BinCounts',histograms{i,j});
            ax = gca;
            disableDefaultInteractivity(ax);
            set(gca,'visible','off');
        end
    end
end

end

