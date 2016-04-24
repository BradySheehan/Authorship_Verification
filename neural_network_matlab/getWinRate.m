function rate = getWinRate(targets, outputs)

outputs(outputs < 0.5) = 0;
outputs(outputs >= 0.5) = 1;

counts = 0;

if(size(targets,1) > 1)
    for ii = 1:size(targets,1)
       if(outputs(ii,1) == targets(ii,1))
           counts = counts + 1;
       end
    end
    rate = (counts/size(targets,1))*100;
else
    for ii = 1:size(targets,2)
       if(outputs(1,ii) == targets(1,ii))
           counts = counts + 1;
       end
    end
    rate = (counts/size(targets,2))*100;
end

end