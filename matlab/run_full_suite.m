function T=run_full_suite(imageFile,outputDir)
% RUN_FULL_SUITE Repeatable image reconstructions and BER/EVM sweeps.
% Project author: Vahab Khalili.
%
% Usage:
%   T=run_full_suite('assets/input_images/lenna.png','results/matlab');
%   T=run_full_suite();  % deterministic synthetic RGB fixture
%
% For every modulation QPSK/16PSK/16QAM, FFT size 16/32/64 and
% sample-domain SNR 0/5/10/15/20/25/30 dB, save recovered image,
% metrics, and summary figures. This is a FRESH reference experiment,
% not a reproduction of the historical Simulink plots.
if nargin<1 || isempty(imageFile)
    [x,y]=meshgrid(uint8(0:63),uint8(0:63));
    imageFile=fullfile(tempdir,'ofdm_synthetic_rgb.png');
    imwrite(cat(3,4*x,4*y,2*x+2*y),imageFile);
end
if nargin<2 || isempty(outputDir),outputDir=fullfile('results','matlab');end
if ~exist(outputDir,'dir'),mkdir(outputDir);end
mods={'QPSK','16PSK','16QAM'};
Ns=[16 32 64];snrs=[0 5 10 15 20 25 30];
n=numel(mods)*numel(Ns)*numel(snrs);
names=cell(n,1);nffts=zeros(n,1);snrValues=zeros(n,1);
bers=zeros(n,1);evms=zeros(n,1);waveP=zeros(n,1);noiseP=zeros(n,1);
row=0;
for m=1:numel(mods)
  for ni=1:numel(Ns)
    N=Ns(ni);
    for si=1:numel(snrs)
      s=snrs(si);row=row+1;
      r=run_ofdm_reference(imageFile,mods{m},N,s,N/4);
      names{row}=mods{m};nffts(row)=N;snrValues(row)=s;
      bers(row)=r.ber;evms(row)=r.evm;
      waveP(row)=r.waveformPower;noiseP(row)=r.noisePower;
      name=sprintf('%s_SNR%02d_N%02d',mods{m},s,N);
      imwrite(r.reconstructedImage,fullfile(outputDir,[name '.png']));
    end
  end
end
T=table(names,nffts,snrValues,bers,evms,waveP,noiseP,...
    'VariableNames',{'Modulation','NFFT','SampleSNRdB','BER','EVM',...
                     'WaveformPower','NoisePower'});
writetable(T,fullfile(outputDir,'case_metrics.csv'));
f=figure('Visible','off','Color','white','Position',[100 100 1200 350]);
for ni=1:numel(Ns)
  subplot(1,3,ni);hold on;grid on;
  for m=1:numel(mods)
    ix=strcmp(names,mods{m}) & nffts==Ns(ni);
    semilogy(snrValues(ix),max(bers(ix),0.5/numel(r.originalBits)),'-o',...
             'DisplayName',mods{m},'LineWidth',1.5);
  end
  title(sprintf('NFFT = %d',Ns(ni)));
  xlabel('Measured-power sample SNR (dB)');ylabel('BER (display floor)');
  legend('Location','northeast');ylim([1e-6 1]);
end
saveas(f,fullfile(outputDir,'BER_sweep.png'));close(f);
% Gallery: Lena (or supplied source) compared with representative reconstructions.
f=figure('Visible','off','Color','white','Position',[100 100 1250 900]);
for m=1:numel(mods)
  for k=1:4
    ax=subplot(3,4,(m-1)*4+k);
    if k==1
      I=imread(imageFile); titleText=sprintf('%s input',mods{m});
    else
      s=[0 10 25];s=s(k-1);
      I=imread(fullfile(outputDir,sprintf('%s_SNR%02d_N64.png',mods{m},s)));
      titleText=sprintf('%s, N64, SNR %d',mods{m},s);
    end
    image(I);axis image off;title(ax,titleText,'Interpreter','none');
  end
end
saveas(f,fullfile(outputDir,'image_gallery.png'));close(f);
fprintf('Saved %d numerical reference scenarios into %s\n',height(T),outputDir);
end
