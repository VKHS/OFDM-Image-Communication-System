function out = prepare_grayscale_bitstream()
    Lena = imread('lena.jpg');
    Lena1 = reshape(Lena,512*512,1);
    Lena2 = dec2bin(Lena1);
    %Lena3 = reshape(Lena2,512*512*8,1);
    out = zeros(1,512*512*8/2);
    kk = 0;
    for ii = 1 : 512*512
        for jj = 1 : 2 : 7
            kk = kk + 1;
            switch Lena2(ii,jj:jj+1)
                case '00'
                    out(kk) = 0;
                case '01'
                    out(kk) = 1;
                case '10'
                    out(kk) = 2;
                case '11'
                    out(kk) = 3;
            end
        end
    end
    
    




% t = linspace(0,1,length(Lena1));
% Step = length(t);
% LenaIn.time = t';
% LenaIn.signals.values = Lena1';