pic=imread('lena.jpg');
VEC = pic(:);
VEC = VEC.';
VEC1=VEC;
OUT;
OUT=OUT.';
OUT=OUT(1,:);
OUT=OUT([2:151876]);
OUT=reshape(OUT,225,225,3);
OUT=uint8(OUT);
imwrite(OUT,'lena_out.jpg')



