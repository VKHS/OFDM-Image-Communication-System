OUT = [OUT1(9:8:262145,:);OUT2(9:8:262145,:);OUT3(9:8:262145,:);OUT4(9:8:262145,:)...
    ;OUT5(9:8:262145,:);OUT6(9:8:262145,:);OUT7(9:8:262145,:);OUT8(9:8:262145,:)];
OUT = reshape(OUT,262144*4,1);
OUT = char(OUT);
LenaOut = bin2dec(OUT);
%  az 9 8 ta 8 ta bardar! 


% Lena = imread('lena.jpg');
% Lena1 = reshape(Lena,512*512,1);
% Lena2 = dec2bin(Lena1);
% % Lena3 = reshape(Lena2,512*512*8,1);
% out = zeros(1,512*512*8/2);
% kk = 0;
% for ii = 1 : 512*512
%     for jj = 1 : 2 : 7
%         kk = kk + 1;
%         switch Lena2(ii,jj:jj+1)
%             case '00'
%                 out(kk) = 0;
%             case '01'
%                 out(kk) = 1;
%             case '10'
%                 out(kk) = 2;
%             case '11'
%                 out(kk) = 3;
%         end
%     end
% end
% M = 4; 
% out2 = reshape(out',M,512*512*8/2/(M));
% Lena1=int8(out2);
% t = length(out2);
% t = 1:1:t;
% tstop = t(end);
% Step = 1;
% LenaIn.time = t;
% LenaIn.signals.values = Lena1';
