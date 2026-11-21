u = size(in); %sent vector size
BitRate = 960;%number of bits per frame (from simulink).
c2(1:u)=simout(BitRate + 1:u + BitRate);% copy simulink output bits to c2 vector
c2 = dec2bin(c2);%0&1 to ASCII codes 
c1 = reshape(c2,[],8);%packing bits by 8
im_out = bin2dec(c1);%binary bits in ASCII format to decimal conversion
im_out = reshape(im_out,m,n,p);%m,n,p are obtained while transmition
im_out = uint8(im_out);%make matrix data format proper for image
subplot(1,2,2)
image(im_out);%show received image
subplot(1,2,1)
image(im)

