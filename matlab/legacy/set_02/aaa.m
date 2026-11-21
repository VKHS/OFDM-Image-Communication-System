clc;clear all;close all;
pic=imread('lena.jpg');
vec = pic(:);
vec = vec.';
vec1=vec;
s = size(vec1,2);
fs = 16;

for i = 0:ceil(s/fs)
   

    fragment = vec1(i*fs + 1:min((i+1)*fs,s));
    if size(fragment,2) == 0
        break
    end
    bitfragment = de2bi(fragment);
    bitfragmentvec=bitfragment(:)';
    x=bitfragmentvec;
    
    
    


end
for j=1:1:2
sim('untitled.slx');
Res{j} = ans;
end