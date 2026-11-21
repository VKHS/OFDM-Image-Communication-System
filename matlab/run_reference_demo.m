% RUN_REFERENCE_DEMO Single-image smoke test (MATLAB only, no Simulink).
% Project author: Vahab Khalili.
% From the repository root: run('matlab/run_reference_demo.m')
thisScript=mfilename('fullpath');
root=fileparts(fileparts(thisScript));
addpath(fullfile(root,'matlab'));
candidate=fullfile(root,'assets','input_images','lenna.png');
if ~exist(candidate,'file')
    fprintf('Historical Lena image not installed; creating deterministic synthetic RGB input.\n');
    [x,y]=meshgrid(uint8(0:63),uint8(0:63));
    synthetic=cat(3,4*x,4*y,2*x+2*y);
    candidate=fullfile(tempdir,'ofdm_synthetic_rgb.png');
    imwrite(synthetic,candidate);
end
mods={'QPSK','16PSK','16QAM'};
Ns=[16,32,64];
for a=1:numel(mods)
    for b=1:numel(Ns)
        N=Ns(b);
        r=run_ofdm_reference(candidate,mods{a},N,Inf,N/4);
        assert(r.ber==0,'Noise-free OFDM bit error!');
        fprintf('%-6s N=%d SNR=Inf BER=%g EVM=%g\n',mods{a},N,r.ber,r.evm);
    end
end
