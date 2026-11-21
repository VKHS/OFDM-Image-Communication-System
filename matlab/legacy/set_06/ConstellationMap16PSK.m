function y = ConstellationMap16PSK(in)
    L = length(in);
    y = zeros(L/4,1);
    for I=1:L/4
      n = bin2dec( char(in(I*4-3:I*4) + '0')' );
      y(I) = exp(1i*pi/8*n);
    end
end

