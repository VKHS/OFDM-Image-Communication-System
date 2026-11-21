lena_pic=imread('lena.jpg');
lena_vector = lena_pic(:);
lena_vector = lena_vector.';
lena_vector_simulink_in=lena_vector;
lena_output;
lena_output=lena_output.';
lena_output=lena_output(1,:);
lena_output=lena_output([2:151876]);
lena_output=reshape(lena_output,225,225,3);
lena_output=uint8(lena_output);
imwrite(lena_output,'lena_out.jpg')



