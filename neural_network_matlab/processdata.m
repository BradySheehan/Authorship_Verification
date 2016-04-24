%This function reads in data generated from the python code in a comma
%seperated list, with each feature vector pair on one row. The data is then
%input to the neural network using the in and out vectors returned.

function [in, out] = processdata()
in1 = importdata('all_diff_pairs.txt');
in2 = importdata('all_same_pairs.txt');
out1 = importdata('out1.txt');
out2 = importdata('out2.txt');
in = cat(1, in1, in2);
out = cat(1, out1, out2);
end
