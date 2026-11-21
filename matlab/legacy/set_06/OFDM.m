clear
Fc = 40e6; % Carrier Frequency
Fadc = 5e6; % input data BaudRate
Nfft_range = [ 64];
% modulation_range=["QPSK" "16QAM" "16PSK"];
modulation_range=["16PSK"];
SNR_range = 40;% white guasian noise added in dB
%% Generat bit stream
im = imread('Lenna_(test_image).png');
im_bin = int8(dec2bin(im(:))');
im_bin = im_bin(:)-'0';
im_bin = im_bin(:); %% input data bit stream
ber = zeros(length(modulation_range) , length(Nfft_range) , length(SNR_range));
for modulation = modulation_range
    for Nfft = Nfft_range
        for SNR = SNR_range
            %% Constellation Mapping and Serial to parallel 
            if modulation == "QPSK"
                X = wlanConstellationMap(im_bin,2);
            elseif modulation == "16QAM"
                X = wlanConstellationMap(im_bin,4);
            elseif modulation == "16PSK"
                X = ConstellationMap16PSK(im_bin);
            end
            %% IFF and parallel to serial
            X_blocks = reshape( X , Nfft , length(X) / Nfft );
            X_I = real( ifft(X_blocks) );
            X_Q = imag( ifft(X_blocks) );
            clear X_blocks 
            %bit stream
            X_I = X_I(:);
            X_Q = X_Q(:);
            N_pac = length(X_I);
            %% Up convesion
            Ts = 1/(5*Fc); %% simulation samplling time
            n_sample = round(1/(Ts * Fadc));
            t = ((0:length(X_I)*n_sample-1)*Ts)';
            % C_I = cos( 2 * pi * Fc * t);
            % C_Q = sin( 2 * pi * Fc * t);
            %%DAC and carrier multiply
            St = kron(X_I , ones(n_sample,1)) .* cos( 2 * pi * Fc * t) + kron(X_Q , ones(n_sample,1)) .* sin( 2 * pi * Fc * t);
            clear X_I X_Q
            %% Channel noise
            Rt = awgn(St,SNR);
            clear St %% free up some memory
            %% reciever
            X_I_rec = Rt .* cos( 2 * pi * Fc * t); %% down convert INPHASE
            X_I_rec = lowpass(X_I_rec,Fadc*2,1/Ts); %% lowpass filter
            X_I_rec = X_I_rec(floor(n_sample/2):n_sample:N_pac*n_sample-floor(n_sample/2)); %% ADC sampling
            % clear C_I 
            X_Q_rec = Rt .* sin( 2 * pi * Fc * t); %% down convert Quadrature
            X_Q_rec = lowpass(X_Q_rec,Fadc*2,1/Ts);
            X_Q_rec = X_Q_rec(floor(n_sample/2):n_sample:N_pac*n_sample-floor(n_sample/2)); %% ADC sampling
            % clear C_Q 
            clear R_T t
            X_rec = X_I_rec + X_Q_rec * 1i;
            clear X_I_rec X_Q_rec
            %% FFT 
            X_rec_blocks = reshape( X_rec , Nfft  , length(X_rec) / Nfft  );
            Y = fft(X_rec_blocks);
            Y = 2*Y(:);
            clear X_rec X_rec_blocks
            %% symbol detection
            if modulation == "QPSK"
                noiseVarEst = 0;
                demapType = 'hard';
                din_rec = int8(wlanConstellationDemap(Y,noiseVarEst,2,demapType));
            elseif modulation == "16QAM"
                noiseVarEst = 0;
                demapType = 'hard';
                din_rec = int8(wlanConstellationDemap(Y,noiseVarEst,4,demapType));
            elseif modulation == "16PSK"
                din_rec = ConstellationDemap16PSK(Y);
            end
            % bit error rate calculation
            beri = sum(abs(im_bin -  din_rec )) / length(im_bin);
            ber(modulation == modulation_range , Nfft == Nfft_range , SNR == SNR_range) = beri;
            im_rec = reshape(din_rec , 8 , 512*512*3);
            im_rec = im_rec + '0';
            im_rec = uint8(bin2dec(char(im_rec')));
            im_rec = reshape(im_rec,512,512,3);
            %%
            lim = 1.5;
            f1 = figure;
            subplot(2,2,1)
            plot(X,'x')
            title(sprintf('Input constellation is %s\nN-FFT = %d', modulation,Nfft))
            xlim([-lim lim])
            ylim([-lim lim])
            axis equal
            subplot(2,2,2)
            plot(Y,'x')
            xlim([-lim lim])
            ylim([-lim lim])
            axis equal
            title(sprintf('Receiver constellation\nSNR = %d\nBit Error Rate =%f',SNR,beri))
            subplot(2,2,3)
            imshow(im);
            title("Input Image");
            subplot(2,2,4)
            imshow(im_rec);
            title("Received Image");
            savefig(sprintf('mod=%s-SNR=%d-NFFT=%d', modulation, SNR,Nfft))
            close(f1)
            disp('mod='+modulation+'-SNR='+SNR+'-NFFT='+Nfft)
        end 
    end
end
%% BER plot
for Nfft = Nfft_range
    figure
    hold on
    for modulation = modulation_range    
        semilogy(SNR_range , squeeze( ber( modulation == modulation_range , Nfft == Nfft_range , :) ) )
    end
    title(sprintf('NFFT=%d',Nfft))
    legend(modulation_range)
    xlabel('SNR(dB)')
    ylabel('Bit Error Rate')
    grid on
end