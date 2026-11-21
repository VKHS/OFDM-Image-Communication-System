dac_im;
dac_re;
adc_im=dac_im;
adc_re=dac_re;
adc_im=adc_im(2,:);
adc_re=adc_re(2,:);

lenajoon;
     

lenajoon=lenajoon.';
lenajoon1=lenajoon(1,:);
lenajoon2=lenajoon1([2:151876]);
lenajoon3=reshape(lenajoon2,225,225,3);
out4=uint8(lenajoon3);
imwrite(lenajoon3,'lenajoon.jpg')