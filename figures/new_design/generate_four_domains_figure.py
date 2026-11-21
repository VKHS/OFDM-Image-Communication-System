import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
p=Path(__file__).resolve().parent
fig,ax=plt.subplots(figsize=(9.2,5.0));ax.set_xlim(0,9);ax.set_ylim(0,5);ax.axis('off')
boxes=[
(.28,2.78,'1  SOURCE & MODULATION','Image bytes  |  bit packing\nConstellation mapping  |  source accuracy','#DCECF4'),
(4.63,2.78,'2  OFDM / FFT HARDWARE','IFFT, FFT and orthogonality\nRadix-2 butterflies  |  serial scheduling','#DCECF4'),
(.28,.35,'3  CONVERTERS & CHANNEL','I/Q processing  |  RF options\nADC/DAC quantization  |  AWGN and SNR','#F5E8D2'),
(4.63,.35,'4  RECEPTION & EVALUATION','Stream alignment  |  demapping\nBER, EVM and image reconstruction','#E9E0F5')]
for x,y,title,body,col in boxes:
 box=FancyBboxPatch((x,y),4.1,2.0,boxstyle='round,pad=.11,rounding_size=.18',linewidth=1.1,edgecolor='#AEC2D0',facecolor=col);ax.add_patch(box)
 ax.text(x+.22,y+1.60,title,weight='bold',color='#17314E',fontsize=13,ha='left')
 ax.text(x+.22,y+.94,body,ha='left',va='center',color='#213A56',fontsize=12.2,linespacing=1.55)
fig.tight_layout(pad=.5);fig.savefig(p/'F02b_domains_report.png',dpi=195);fig.savefig(p/'F02b_domains_report.svg');plt.close(fig)
