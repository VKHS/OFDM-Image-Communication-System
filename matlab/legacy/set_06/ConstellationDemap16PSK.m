function y = ConstellationDemap16PSK(in)
    ref = exp(1i*pi/8*(0:15));
    L = length(in);
    y = zeros(L*4,1,'int8');
    for i=1:L
        error = abs(ref - in(i));
        [m ,  id] = min(error); 
        y(i*4-3:i*4) = (dec2bin( id - 1 , 4) - '0')';
    end
end