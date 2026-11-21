function result = run_ofdm_reference(imageFile, modulation, N, snrDb, cpLen)
% RUN_OFDM_REFERENCE Reversible image transmission in a complex-baseband OFDM link.
% Project author: Vahab Khalili.
% New numerical reference; it is not the original Simulink hardware implementation.
% Example:
%   r=run_ofdm_reference('lena.png','16QAM',64,12,16);
%
% This source uses base MATLAB; no Communications Toolbox is needed.
if nargin < 5, cpLen=N/4; end
assert(ismember(N,[16,32,64]) && cpLen == floor(cpLen) && cpLen>=0 && cpLen<=N);
A=imread(imageFile);
originalSize=size(A);
origBytes=uint8(A(:));
originalBits=reshape((dec2bin(origBytes,8).'-'0'),[],1);
originalBits=double(originalBits);
switch upper(modulation)
    case 'QPSK', M=4;
    case {'16PSK','16QAM'}, M=16;
    otherwise, error('Use QPSK, 16PSK, or 16QAM');
end
bitsPerSymbol=log2(M);
frameBits=N*bitsPerSymbol;
padding=mod(-numel(originalBits),frameBits);
bits=[originalBits;zeros(padding,1)];
groups=reshape(bits,bitsPerSymbol,[]).';
labels=groups*(2.^(bitsPerSymbol-1:-1:0)).';
C=localConstellation(upper(modulation));
X=reshape(C(labels+1),N,[]);
xf=ifft(X,[],1);
if cpLen>0, tx=[xf(end-cpLen+1:end,:);xf];else,tx=xf;end
power=mean(abs(tx(:)).^2);
if isinf(snrDb)
    noise=zeros(size(tx)); noisePower=0;
else
    rng(12345,'twister');
    noisePower=power/10^(snrDb/10);
    noise=sqrt(noisePower/2)*(randn(size(tx))+1j*randn(size(tx)));
end
rx=tx+noise;
if cpLen>0,rx=rx(cpLen+1:end,:);end
Y=fft(rx,[],1);Y=Y(:);
nearestLabels=zeros(numel(Y),1);
best=inf(numel(Y),1);
for k=1:numel(C)
    distances=abs(Y-C(k)).^2;
    mask=distances<best;
    nearestLabels(mask)=k-1;
    best(mask)=distances(mask);
end
receivedBits=reshape((dec2bin(nearestLabels,bitsPerSymbol).'-'0'),[],1);
receivedBits=double(receivedBits(1:numel(originalBits)));
receivedBytes=uint8(bin2dec(char(reshape(receivedBits,8,[]).'+ '0')));
receivedImage=reshape(receivedBytes,originalSize);
result.modulation=upper(modulation);
result.fftLength=N;
result.cpLength=cpLen;
result.snrDb=snrDb;
result.paddingBits=padding;
result.waveformPower=power;
result.noisePower=noisePower;
result.ber=mean(originalBits~=receivedBits);
result.evm=sqrt(mean(abs(Y-X(:)).^2)/mean(abs(X(:)).^2));
result.reconstructedImage=receivedImage;
result.sourceImage=A;
result.originalBits=originalBits;
result.receivedBits=receivedBits;
result.constellation=C;
result.rxSymbols=Y;
result.txSymbols=X(:);
end

function C=localConstellation(modulation)
switch modulation
    case 'QPSK'
        C=exp(1j*(pi/4+[0 1 3 2]*pi/2));
    case '16PSK'
        C=zeros(16,1);
        pos=0:15;labels=bitxor(uint32(pos),bitshift(uint32(pos),-1));
        C(double(labels)+1)=exp(1j*2*pi*pos/16);
    case '16QAM'
        a=[-3 -1 3 1]/sqrt(10);
        C=zeros(16,1);
        for n=0:15
            C(n+1)=a(floor(n/4)+1)+1j*a(mod(n,4)+1);
        end
end
C=C(:);
end
