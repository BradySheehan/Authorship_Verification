function result = network_parameter_testing()
dbstop if error
[in, out] = processdata();
trainFcn = {'trainscg', 'traincgb', 'traincgf', 'traincgp'};
hiddenLayerSize = [10:25, 35, 50, 100];
save('testing_data', 'in', 'out', 'trainFcn', 'hiddenLayerSize');
ind = 1;
for ii = 1:length(trainFcn)
    t = trainFcn{1, ii};
    for jj = 1:length(hiddenLayerSize)
        h = hiddenLayerSize(1, jj);
        [net,outputs, performance, percentCorrect, trainFcn2, hiddenLayerSize2] = pattern_network(in, out, t, h);
        save(sprintf('%s%d', '2network', ind), 'net', 'outputs', 'performance', 'percentCorrect', 'trainFcn2', 'hiddenLayerSize2');
        ind = ind + 1;
        close all;
    end
end

end