%% sections for parallel QPSK, 16PSK, and 16QAM
%% before Simulink, For QPSK 16 Point
clear all
A=imread('Lenna_(test_image).png');
B=double(reshape(A,512*512*3/4,4));
L=length(B);
t=1:L;
t1=t.';
simin=[t1 B];
image(A)

%% after Simulink QPSK/16PSK/16QAM 16/32/64 Point
dd=demQ;
dd(1,:)=[];
ima=uint8(reshape(dd,512,512,3));
image(ima)

%% before Simulink, For QPSK 32 Point & 16PSK/16QAM 16 point
clear all
A=imread('Lenna_(test_image).png');
B=double(reshape(A,512*512*3/8,8));
L=length(B);
t=1:L;
t1=t.';
simin=[t1 B];
% image(A)

%% after Simulink QPSK/16PSK/16QAM 16/32/64 Point
dd=demQ;
dd(1,:)=[];
ima=uint8(reshape(dd,512,512,3));
image(ima)

%% before Simulink, For QPSK 64 Point & 16PSK/16QAM 32 point
clear all
A=imread('Lenna_(test_image).png');
B=double(reshape(A,512*512*3/16,16));
L=length(B);
t=1:L;
t1=t.';
simin=[t1 B];
% image(A)

%% after Simulink QPSK/16PSK/16QAM 16/32/64 Point
dd=demQ;
dd(1,:)=[];
ima=uint8(reshape(dd,512,512,3));
image(ima)

%% before Simulink, For 16PSK/16QAM 64 point
clear all
A=imread('Lenna_(test_image).png');
B=double(reshape(A,512*512*3/32,32));
L=length(B);
t=1:L;
t1=t.';
simin=[t1 B];
% image(A)

%% after Simulink QPSK/16PSK/16QAM 16/32/64 Point
dd=demQ;
dd(1,:)=[];
ima=uint8(reshape(dd,512,512,3));
image(ima)

