function result = network_parameter_plots()

file_list = get_all_files('/home/fa13sheehan/Desktop/AI_Project-master/text_processing_python');
ind = 1;

hiddenLayerSize = [10:25, 35, 50, 100];
xplot = 1:length(hiddenLayerSize);

for file = file_list(:)'
    [pathstr, name, ext] = fileparts(char(file));
    if(strcmp(ext,'.mat') && length(strfind(name, '2network'))~=0)
        load(char(file));
        %we want to plot stuff for each training function
        %plot one training function with percent correct on y axis and
        %number of hidden layers on x axis
        perf_value(ind) = performance;
        rate(ind) = percentCorrect;
        trainFcn2
        if(ind == length(hiddenLayerSize))
            figure
            subplot(2,1,1)
            bar(xplot, perf_value, 0.5), xlabel('number of hidden layers 10:25, 35, 50, 100'), ylabel('performance with respect to MSE');
            title({sprintf('%s%s', 'Neural network performance with trainFcn= ', char(net.trainFcn)), sprintf('%s%d', ' min value = ', min(perf_value))})
            set(gca, 'XTick', xplot);
            set(gca, 'XTickLabel', xplot);
            subplot(2,1,2)
            bar(xplot, rate, 0.5), xlabel('number of hidden layers, 10:25, 35, 50, 100'), ylabel('rate of correct classifications');
            title({sprintf('%s%s', 'Neural network correct classification rate with trainFcn= ', char(net.trainFcn)), sprintf('%s%d', 'max value = ', max(rate))})
           set(gca, 'XTick', xplot);
            set(gca, 'XTickLabel', xplot);
            ind = 1;
        end
        ind = ind + 1;
        
    end
end

end