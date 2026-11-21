function test_smoke()
% TEST_SMOKE Quick MATLAB assertions for the full reversible image link.
% Project author: Vahab Khalili.
img=uint8(reshape(mod(0:3*32*32-1,256),32,32,3));
file=fullfile(tempdir,'ofdm_matlab_smoke.png');
imwrite(img,file);
mods={'QPSK','16PSK','16QAM'};Ns=[16 32 64];
for m=1:numel(mods)
    for n=1:numel(Ns)
        r=run_ofdm_reference(file,mods{m},Ns(n),Inf,Ns(n)/4);
        assert(r.ber==0,'Incorrect BER for an ideal channel');
        assert(isequal(r.reconstructedImage,img),'Image bytes differ');
        assert(r.evm<1e-10,'Numerical FFT error too large');
    end
end
fprintf('PASS: nine noise-free MATLAB image transmission scenarios.\n');
end
