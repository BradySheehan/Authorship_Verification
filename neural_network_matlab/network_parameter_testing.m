function network_parameter_testing()
[in, out] = processdata();
trainFcn = {'trainscg','traincgb','traincgf','traincgp','trainlm','trainbr','trainrp'};
hiddenLayerSize = [10, 12, 15, 20, 25, 35, 60, 75, 100, 250];
ind = 1;
for ii = 1:length(trainFcn)
    t = trainFcn{1, ii};
    for jj = 1:length(hiddenLayerSize)
        h = hiddenLayerSize(1, jj);
        [net,outputs, performance, percentCorrect, trainFcn2, hiddenLayerSize2] ...
            = pattern_network(in, out, t, h); %#ok<*ASGLU>
        save(sprintf('%s%d', '2network', ind), 'net', 'outputs', 'performance', ...
            'percentCorrect', 'trainFcn2', 'hiddenLayerSize2');
        ind = ind + 1;
        close all;
    end
end
end
