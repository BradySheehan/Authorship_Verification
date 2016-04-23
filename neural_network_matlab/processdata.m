function [in, out] = processdata()
in1 = importdata('ina3.txt');
in2 = importdata('inb3.txt');
out1 = importdata('outa3.txt');
out2 = importdata('outb3.txt');

in = cat(1, in1, in2);
out = cat(1, out1, out2);

end
