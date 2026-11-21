%% For Serial QPSK 16PSK 16QAM
%% For QPSK Serial Before Simulink
clear all
A=imread('Lenna_(test_image).png');
image(A)
B=double(reshape(A,512*512*3,1));
Bb=de2bi(B,8);
C=double(reshape(Bb,786432*4,2));
L=length(C);
t=1:L;
tt=t;
t1=tt.';
simin=[t1 C];

%% SerilaL QPSK after Simiuink 16point
dd=demQ1;
for x=1:51
dd(1,:)=[];
end

dd(3145729,:)=[];
dd(3145729,:)=[];

ddd=double(reshape(dd,786432,8));
dddd=bi2de(ddd);
ima=uint8(reshape(dddd,512,512,3));
image(ima)

%% For 16PSK/16QAM Serial Before Simulink
clear all
A=imread('Lenna_(test_image).png');
image(A)
B=double(reshape(A,512*512*3,1));
Bb=de2bi(B,8);
C=double(reshape(Bb,786432*2,4));
L=length(C);
t=1:L;
tt=t;
t1=tt.';
simin=[t1 C];

%% SerilaL 16PSK/16QAM after Simiuink 16point
dd=demQ1;
for x=1:51
dd(1,:)=[];
end

dd(1572865,:)=[];
dd(1572865,:)=[];

ddd=double(reshape(dd,786432,8));
dddd=bi2de(ddd);
ima=uint8(reshape(dddd,512,512,3));
image(ima)


%% SerilaL 16PSK/16QAM after Simiuink 32point
dd=demQ1;
for x=1:107
dd(1,:)=[];
end

dd(1572865,:)=[];
dd(1572865,:)=[];

ddd=double(reshape(dd,786432,8));
dddd=bi2de(ddd);
ima=uint8(reshape(dddd,512,512,3));
image(ima)


%% SerilaL 16PSK/16QAM after Simiuink 64point
dd=demQ1;
for x=1:227
dd(1,:)=[];
end

dd(1572865,:)=[];
dd(1572865,:)=[];

ddd=double(reshape(dd,786432,8));
dddd=bi2de(ddd);
ima=uint8(reshape(dddd,512,512,3));
image(ima)

