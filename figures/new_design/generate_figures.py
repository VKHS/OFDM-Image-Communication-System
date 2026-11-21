#!/usr/bin/env python3
"""Generate editable vector (SVG/DOT) and publication-resolution PNG diagrams."""
from pathlib import Path
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
ROOT=Path(__file__).resolve().parent
navy='#17314E';teal='#117C8B';orange='#B5631F';pale='#EAF2F7';purple='#7754A6';dark='#243342';grey='#5C6A76';red='#AD3B3B';green='#26805B'

def graph(name,src):
    dot=ROOT/(name+'.dot');dot.write_text(src,encoding='utf8')
    for ext in ('svg','png'):
        subprocess.run(['dot',f'-T{ext}',str(dot),'-o',str(ROOT/(name+'.'+ext))],check=True)

settings=f'''graph [bgcolor="white",ranksep="0.7",nodesep="0.25",fontname="DejaVu Sans",fontsize="12",pad="0.3",splines="ortho"]; node [fontname="DejaVu Sans",fontcolor="{navy}",fontsize="10",shape="box",style="rounded,filled",color="#CAD7E0",fillcolor="{pale}",margin="0.14,0.08"]; edge [color="{grey}",arrowsize="0.65",penwidth="1.2",fontname="DejaVu Sans",fontsize="9"];'''

graph('F01_complete_system',f'''digraph X {{ {settings} rankdir=LR;
 subgraph cluster_0 {{label="DATA & MAPPING";color="#DBE9EF";a[label="Source image"];b[label="Byte / bit serializer"];c[label="QPSK / 16-PSK / 16-QAM"];a->b->c;}}
 subgraph cluster_1 {{label="OFDM TRANSMITTER";color="#DBE9EF";d[label="Group N symbols\n+ optional null bins"];e[label="N-point IFFT"];f[label="Append cyclic prefix\n(if enabled)"];d->e->f;}}
 subgraph cluster_2 {{label="PHYSICAL / CHANNEL MODEL";color="#DBE9EF";g[label="Complex baseband\nor I/Q DAC + RF"];h[label="AWGN; optional\nquantization / nonidealities"];g->h;}}
 subgraph cluster_3 {{label="OFDM RECEIVER";color="#DBE9EF";i[label="Recover I/Q samples"];j[label="Remove prefix"];k[label="N-point FFT"];l[label="Extract occupied bins"];i->j->k->l;}}
 subgraph cluster_4 {{label="DATA & EVALUATION";color="#DBE9EF";m[label="Constellation decisions"];n[label="Bit / byte unpacking"];o[label="Recovered image"];p[label="BER / EVM / image quality",fillcolor="#E9F4EC",color="{green}"];m->n->o;n->p;}}
 c->d;f->g;h->i;l->m;b->p[style=dashed,label="reference bits"];}}
''')

graph('F02_four_design_domains',f'''digraph X {{{settings} rankdir=TB; center[shape=ellipse,fillcolor="{navy}",fontcolor="white",label="OFDM IMAGE COMMUNICATION\nWITH SERIAL FFT HARDWARE",fontsize=15,margin="0.3,0.2"];
 a[fillcolor="#D8EBF3",label="I. SOURCE & MODULATION\nImage bytes; MSB/LSB ordering\nConstellations; symbol packing"];
 b[fillcolor="#D8EBF3",label="II. OFDM / FFT HARDWARE\nN-point IFFT/FFT; butterflies\nTwiddles; SDF delays; ordering"];
 c[fillcolor="#F6ECD6",label="III. CONVERTERS & CHANNEL\nI/Q paths; finite precision\nAWGN; optional RF and prefix"];
 d[fillcolor="#E8E0F4",label="IV. RX, VERIFICATION & RESULTS\nDemap; byte/image reconstruction\nBER; SNR calibration; timing"];
 {{rank=same;a;b;}};{{rank=same;c;d;}};center->a;center->b;center->c;center->d;
}}''')

graph('F03_serial_fft_pipeline',f'''digraph X {{{settings} rankdir=LR;
 in[label="1 complex sample / cycle",fillcolor="#E6F4EF"];
 s1[label="Stage 1\nDelay 8\nButterfly + W",fillcolor="#D9EAF2"];
 s2[label="Stage 2\nDelay 4\nButterfly + W",fillcolor="#D9EAF2"];
 s3[label="Stage 3\nDelay 2\nButterfly + W",fillcolor="#D9EAF2"];
 s4[label="Stage 4\nDelay 1\nButterfly + W",fillcolor="#D9EAF2"];
 order[label="Reorder / output alignment",fillcolor="#F6ECD6"];
 out[label="1 complex result / cycle\nafter pipeline fill",fillcolor="#E6F4EF"];
 in->s1->s2->s3->s4->order->out;
 ctrl[label="Counter + stage switching\nand coefficient address",fillcolor="#EEE7F6",color="{purple}"];
 ctrl->s1[style=dashed];ctrl->s2[style=dashed];ctrl->s3[style=dashed];ctrl->s4[style=dashed];
}}''')

graph('F04_butterfly_and_scheduling',f'''digraph X {{{settings} rankdir=LR; node [shape=box];
 x0[label="Arriving sample a\n(or delayed prior sample)"];
 x1[label="Arriving sample b\n(or feedback data)"];
 plus[label="Complex add\nu = a + b",fillcolor="#D9EAF2"];
 minus[label="Complex subtract\nd = a - b",fillcolor="#D9EAF2"];
 tw[label="Twiddle multiply\nv = d · W(k,N)",fillcolor="#E8E0F4"];
 mem[label="Delay / feedback\nand bypass switching",fillcolor="#F6ECD6"];
 x0->plus;x1->plus;x0->minus;x1->minus;minus->tw;plus->mem;tw->mem;
 counter[label="Cycle counter\nstage / twiddle controls",fillcolor="#EEE7F6"];
 counter->mem[style=dashed];counter->tw[style=dashed];
}}''')

graph('F05_baseband_vs_rf',f'''digraph X {{{settings} rankdir=TB;
 tx[label="IFFT output x[n] = I[n] + jQ[n]",fillcolor="#D9EAF2"];
 split[label="Separate I / Q"]; tx->split;
 a[label="I DAC / hold"];b[label="Q DAC / hold"];split->a;split->b;
 c[label="× cos(2πfct)"];d[label="× sin(2πfct)"];a->c;b->d;
 sum[label="Sum real RF waveform\ns(t) = I(t)cos + Q(t)sin",fillcolor="#F6ECD6"];c->sum;d->sum;
 chan[label="RF channel + Gaussian noise"];sum->chan;
 mix[label="Coherent I / Q downconversion"];chan->mix;
 filt[label="Low-pass filtering and sampling"];mix->filt;
 recomb[label="I + jQ --> FFT --> decisions",fillcolor="#D9EAF2"];filt->recomb;
}}''')

graph('F06_data_representation',f'''digraph X {{{settings} rankdir=LR;
 im[label="RGB / grayscale image\npixel values 0...255"];
 by[label="Byte vector\n(e.g. 173)"];
 bits[label="MSB-first bits\n10101101"];
 q[label="QPSK: 10 | 10 | 11 | 01\n4 symbols / 8-bit value",fillcolor="#D9EAF2"];
 p[label="16-PSK or 16-QAM\n1010 | 1101\n2 symbols / 8-bit value",fillcolor="#E8E0F4"];
 post[label="Demap --> regroup 8 bits\n--> restore original array",fillcolor="#F6ECD6"];
 im->by->bits;bits->q;bits->p;q->post;p->post;
}}''')

graph('F07_validation_ladder',f'''digraph X {{{settings} rankdir=TB;
 a[label="Level 1: Bit-packing inverse\nidentical original and reconstructed byte vectors",fillcolor="#E6F4EF"];
 b[label="Level 2: Numerical FFT/IFFT\nmax|FFT(IFFT(X)) - X| within tolerance",fillcolor="#E6F4EF"];
 c[label="Level 3: Noiseless end-to-end link\nBER = 0; reconstructed image exact",fillcolor="#E6F4EF"];
 d[label="Level 4: AWGN and precision sweeps\nmeasured signal power; BER; EVM; PSNR",fillcolor="#F6ECD6"];
 e[label="Level 5: Cycle-accurate serial verification\nstage timing, ordering, latency, overflow",fillcolor="#F6ECD6"];
 f[label="Level 6: Synthesized / measured hardware\nresources, timing, frequency, power",fillcolor="#EEE7F6"];
 a->b->c->d->e->f;
}}''')

graph('F08_limited_claims',f'''digraph X {{{settings} rankdir=LR;
 a[label="Archive contains simulations, images,\nFFT screenshots, and scripts",fillcolor="#D9EAF2"];
 b[label="Demonstrates communication behavior\nand architecture concepts",fillcolor="#E6F4EF"];
 c[label="Does NOT by itself establish\nfull system FPGA deployment,\nphysical power, or bit-exact RTL",fillcolor="#F8E2DF",color="{red}"];
 a->b->c;
}}''')

# Mathematical, properly labeled figures
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.titlesize':12})
fig,axs=plt.subplots(1,3,figsize=(11.8,4.0))
for ax,mode in zip(axs,['QPSK','16-PSK','16-QAM']):
 if mode=='QPSK':
  data=np.exp(1j*(np.pi/4+np.arange(4)*np.pi/2))
 elif mode=='16-PSK':data=np.exp(1j*(np.arange(16)*np.pi/8))
 else:
  coords=[-3,-1,1,3];data=np.array([complex(x,y) for y in coords for x in coords])/np.sqrt(10)
 ax.scatter(data.real,data.imag,s=58,c=teal,edgecolors=navy)
 ax.axhline(0,color='#CBD5DE',linewidth=.8);ax.axvline(0,color='#CBD5DE',linewidth=.8)
 ax.set_aspect('equal');ax.set(xlim=(-1.5,1.5),ylim=(-1.5,1.5),xlabel='In-phase (I)',ylabel='Quadrature (Q)',title=mode)
 ax.grid(alpha=.18)
fig.suptitle('Figure F09 | Constellation geometries (unit mean symbol energy)',fontsize=14)
fig.tight_layout();fig.savefig(ROOT/'F09_constellations.png',dpi=200);fig.savefig(ROOT/'F09_constellations.svg');plt.close(fig)

fig,axs=plt.subplots(2,1,figsize=(11.8,6.0),gridspec_kw={'height_ratios':[1.1,1]})
ax=axs[0]
N=64;occupied=48
for k in range(N):
  col=teal if k<occupied else '#B9C6CF'
  ax.vlines(k,0,1 if k<occupied else .18,color=col,linewidth=2.1)
ax.set(xlim=(-1,64),ylim=(0,1.22),ylabel='Illustrative amplitude',title='64 frequency bins: 48 occupied data carriers + 16 illustrative nulls')
ax.set_xticks([0,15,31,47,48,63]);ax.grid(alpha=.18)
ax=axs[1]
ax.add_patch(Rectangle((0,.3),16,.5,facecolor='#F8E2DF',edgecolor=red))
ax.add_patch(Rectangle((16,.3),64,.5,facecolor='#D9EAF2',edgecolor=navy))
ax.annotate('16-sample cyclic prefix\n(copy of final 16 useful samples)',(8,.55),ha='center',va='center',fontsize=10)
ax.annotate('64 useful time-domain samples', (48,.55),ha='center',va='center',fontsize=11)
ax.set(xlim=(-2,82),ylim=(0,1),xlabel='Sample index within transmitted OFDM symbol',yticks=[],title='Time domain: 64 useful samples + 16-sample cyclic prefix = 80 transmitted samples')
for spine in ax.spines.values():spine.set_visible(False)
fig.tight_layout();fig.savefig(ROOT/'F10_ofdm_framing.png',dpi=200);fig.savefig(ROOT/'F10_ofdm_framing.svg');plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(11.8,4.1))
for ax,N in zip(axs,[16,64]):
 stages=int(np.log2(N)); delys=[N//(2**k) for k in range(1,stages+1)]
 ax.barh(range(stages),delys,color=teal,height=.55)
 for k,n in enumerate(delys):ax.text(n+0.2,k,str(n),va='center')
 ax.set(yticks=range(stages),yticklabels=[f'Stage {k+1}' for k in range(stages)],xlabel='Complex-sample delay depth',title=f'N={N}, total conceptual feedback = {sum(delys)}')
 ax.invert_yaxis();ax.set_xlim(0,max(delys)*1.25);ax.grid(axis='x',alpha=.15)
fig.suptitle('Figure F11 | Conceptual R2SDF feedback storage (does not include reorder / control buffers)',fontsize=13)
fig.tight_layout();fig.savefig(ROOT/'F11_stage_delays.png',dpi=190);fig.savefig(ROOT/'F11_stage_delays.svg');plt.close(fig)

snr=np.array([10,13,16]);ber=np.array([0.0584,0.01727,0.002459])
fig,ax=plt.subplots(figsize=(8.8,4.2))
ax.semilogy(snr,ber,'o-',linewidth=2,color=teal,markersize=7)
for x,y in zip(snr,ber):ax.annotate(f'{y:.5g}',(x,y),xytext=(5,8),textcoords='offset points')
ax.set(xlabel='SNR reported in historical serial 16-QAM example (dB)',ylabel='Reported BER',title='Figure F12 | Reported 16-point, 14-bit serial 16-QAM results')
ax.set_xticks(snr);ax.grid(which='both',alpha=.25)
ax.text(.02,.04,'Numbers reproduced from archived screenshots; not independently rerun.',transform=ax.transAxes,fontsize=9,color=grey)
fig.tight_layout();fig.savefig(ROOT/'F12_reported_ber.png',dpi=195);fig.savefig(ROOT/'F12_reported_ber.svg');plt.close(fig)

N=np.array([16,32,64]);p=1/N
fig,ax=plt.subplots(figsize=(9,4.5))
ax.plot(N,10*np.log10(p),'-o',color=teal,lw=2)
for n,y in zip(N,10*np.log10(p)):ax.annotate(f'{y:.2f} dB',(n,y),xytext=(0,9),textcoords='offset points',ha='center')
ax.set(xlabel='IFFT length N',ylabel='Mean complex sample power for unit-energy, fully occupied bins (dB)',title='Figure F13 | IFFT normalization changes time-sample power at fixed symbol energy')
ax.set_xticks(N);ax.grid(alpha=.18)
fig.tight_layout();fig.savefig(ROOT/'F13_power_scaling.png',dpi=200);fig.savefig(ROOT/'F13_power_scaling.svg');plt.close(fig)

print('Generated conceptual design figures:',len(list(ROOT.glob('*.png'))),'PNG and',len(list(ROOT.glob('*.svg'))),'SVG')
