from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
DIR=Path(__file__).resolve().parent
blue='#17314e';fill_tx='#DBEEF4';fill_rx='#E9E2F3';fill_ch='#F4E6D1';dark='#34485C';
def add(ax,x,y,w,h,caption,fill,fontsize=12):
 p=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.08,rounding_size=0.12',linewidth=1.1,edgecolor='#9FB3C2',facecolor=fill);ax.add_patch(p)
 ax.text(x+w/2,y+h/2,caption,ha='center',va='center',fontsize=fontsize,color=blue,weight='medium')
def arrow(ax,x1,y1,x2,y2):
 ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=15,linewidth=1.4,color=dark))

def make(name,top,bottom):
 fig,ax=plt.subplots(figsize=(12,4.8))
 ax.set_xlim(0,12);ax.set_ylim(0,4.8);ax.axis('off')
 xx=[.3,2.3,4.3,6.3,8.3,10.3]
 for i,t in enumerate(top):
  add(ax,xx[i],3.15,1.45,1.0,t,fill_tx,fontsize=11)
  if i<5:arrow(ax,xx[i]+1.5,3.65,xx[i+1]-.12,3.65)
 for i,t in enumerate(bottom):
  add(ax,xx[i],.65,1.45,1.0,t,fill_rx,fontsize=11)
  if i<5:arrow(ax,xx[i+1]-.13,1.15,xx[i]+1.52,1.15)
 arrow(ax,11.03,3.05,11.03,1.75)
 add(ax,9.55,2.15,1.9,.52,'AWGN / RF channel',fill_ch,10.5)
 ax.text(.2,4.50,'TRANSMITTER',fontsize=14,color=blue,weight='bold')
 ax.text(.2,1.93,'RECEIVER',fontsize=14,color=blue,weight='bold')
 fig.tight_layout(pad=.3);fig.savefig(DIR/(name+'.png'),dpi=185);fig.savefig(DIR/(name+'.svg'));plt.close(fig)

make('F01b_system_report',
 ['Source\nimage','Serialize\n8-bit bytes','Constellation\nQPSK / PSK / QAM','Populate\nOFDM bins','IFFT\n(N points)','CP + I/Q\npath'],
 ['Recovered\nimage','Assemble\nbytes','Symbol-to-bit\ndecisions','Select data\nbins','FFT\n(N points)','I/Q recovery\nremove CP'])
make('F05b_rf_path_report',
 ['IFFT output\nI[n] + jQ[n]','Separate I/Q\nDAC & hold','Modulate I cos\nand Q sin','Sum RF\ncarrier','Passband\nwaveform','Channel input\nI/Q RF'],
 ['FFT input\nI + jQ','Combine\nI and Q','ADC sampling\nI/Q values','Low-pass I/Q\nfiltering','Mix down with\ncosine/sine','Received RF\nwaveform'])
print('created compact report figures')
