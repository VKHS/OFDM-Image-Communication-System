clear
clc
%load image to im matrix (mXnX3)
im = imread('lenna.png');
x = size(im);%number of raws and columns of im matrix
m = x(1);% nummber of raws
n = x(2);% number of columns
p = x(3);%number of pages
b1 = dec2bin(im(:));
b2 = b1(:);
in = b2 - 48;
ts1 = timeseries(in);


