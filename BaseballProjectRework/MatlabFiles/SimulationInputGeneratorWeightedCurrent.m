% this file generates the input for BaseballSimulator.  it will read the
% excel files in MATLAB Inputs and generate a 20x1000 matrix of outcomes
% for each pitcher and hitter.  

function simulationinput = SimulationInputGeneratorWeightedCurrent(inputfile,abcw,apcw,hbcw,hpcw,pw)

%cd('C:\Users\Aaron\Documents\BaseballProjectRework\DailyLineUps\20140419E')
excelinput=round(1000*xlsread(inputfile));
%cd('C:\Users\Aaron\Documents\BaseballProject\MATLAB Files')

%abcw = 1; % awaybattingcareerweight
abaw = 1 - abcw; % awaybattingawayweight
%apcw = 1;
apaw = 1 - apcw;

%hbcw = 1;
hbhw = 1 - hbcw;
%hpcw = 1;
hphw = 1 - hpcw;

%pw = 1;
bw = 1 - pw;

awaybatting=zeros(9,round(bw*1000));
awaypitching=zeros(1,round(pw*1000));
homebatting=zeros(9,round(bw*1000));
homepitching=zeros(1,round(pw*1000));

for i = 1:9
    
    % outcome = batting weight(away batting career weight * career outcome
    %+ away batting away weight * away outcome)
    awalks = round(bw*(abcw*excelinput(i,1)+abaw*excelinput(i,17)));
    asingles = round(bw*(abcw*excelinput(i,2)+abaw*excelinput(i,18)));
    adoubles = round(bw*(abcw*excelinput(i,3)+abaw*excelinput(i,19)));
    atriples = round(bw*(abcw*excelinput(i,4)+abaw*excelinput(i,20)));
    ahrs = round(bw*(abcw*excelinput(i,5)+abaw*excelinput(i,21)));
    asos = round(bw*(abcw*excelinput(i,6)+abaw*excelinput(i,22)));
    agos = round(bw*(abcw*excelinput(i,7)+abaw*excelinput(i,23)));
    %afos = round(bw*(abcw*excelinput(i,8)+abaw*excelinput(i,24)));
    afos = length(awaybatting) - (awalks + asingles + adoubles + atriples + ahrs...
        + asos + agos); % ensures awaybatting has length 1000
    awaybatting(i,:) = [ones(1,awalks) 2*ones(1,asingles) 3*ones(1,adoubles)...
        4*ones(1,atriples) 5*ones(1,ahrs) 6*ones(1,asos) 7*ones(1,agos)...
        8*ones(1,afos)];
      
    
    hwalks = round(bw*(hbcw*excelinput(10+i,1)+hbhw*excelinput(10+i,9)));
    hsingles = round(bw*(hbcw*excelinput(10+i,2)+hbhw*excelinput(10+i,10)));
    hdoubles = round(bw*(hbcw*excelinput(10+i,3)+hbhw*excelinput(10+i,11)));
    htriples = round(bw*(hbcw*excelinput(10+i,4)+hbhw*excelinput(10+i,12)));
    hhrs = round(bw*(hbcw*excelinput(10+i,5)+hbhw*excelinput(10+i,13)));
    hsos = round(bw*(hbcw*excelinput(10+i,6)+hbhw*excelinput(10+i,14)));
    hgos = round(bw*(hbcw*excelinput(10+i,7)+hbhw*excelinput(10+i,15)));
    %afos = round(bw*(abcw*excelinput(i,8)+abaw*excelinput(i,16)));
    hfos = length(homebatting) - (hwalks + hsingles + hdoubles + htriples + hhrs...
        + hsos + hgos); % ensures homebatting has length 1000
    homebatting(i,:) = [ones(1,hwalks) 2*ones(1,hsingles) 3*ones(1,hdoubles) ...
        4*ones(1,htriples) 5*ones(1,hhrs) 6*ones(1,hsos) 7*ones(1,hgos)...
        8*ones(1,hfos)];
    
    
end


awalks = round(pw*(apcw*excelinput(10,1)+apaw*excelinput(10,17)));
asingles = round(pw*(apcw*excelinput(10,2)+apaw*excelinput(10,18)));
adoubles = round(pw*(apcw*excelinput(10,3)+apaw*excelinput(10,19)));
atriples = round(pw*(apcw*excelinput(10,4)+apaw*excelinput(10,20)));
ahrs = round(pw*(apcw*excelinput(10,5)+apaw*excelinput(10,21)));
asos = round(pw*(apcw*excelinput(10,6)+apaw*excelinput(10,22)));
agos = round(pw*(apcw*excelinput(10,7)+apaw*excelinput(10,23)));
afos = length(awaypitching) - (awalks + asingles + adoubles + atriples + ahrs...
    + asos + agos); % ensures awaypitching has length 1000
awaypitching(1,:) = [ones(1,awalks) 2*ones(1,asingles) 3*ones(1,adoubles)...
        4*ones(1,atriples) 5*ones(1,ahrs) 6*ones(1,asos) 7*ones(1,agos)...
        8*ones(1,afos)];

hwalks = round(pw*(hpcw*excelinput(20,1)+hphw*excelinput(20,9)));
hsingles = round(pw*(hpcw*excelinput(20,2)+hphw*excelinput(20,10)));
hdoubles = round(pw*(hpcw*excelinput(20,3)+hphw*excelinput(20,11)));
htriples = round(pw*(hpcw*excelinput(20,4)+hphw*excelinput(20,12)));
hhrs = round(pw*(hpcw*excelinput(20,5)+hphw*excelinput(20,13)));
hsos = round(pw*(hpcw*excelinput(20,6)+hphw*excelinput(20,14)));
hgos = round(pw*(hpcw*excelinput(20,7)+hphw*excelinput(20,15)));
hfos = length(homepitching) - (hwalks + hsingles + hdoubles + htriples + hhrs...
        + hsos + hgos); 

homepitching(1,:) = [ones(1,hwalks) 2*ones(1,hsingles) 3*ones(1,hdoubles) ...
        4*ones(1,htriples) 5*ones(1,hhrs) 6*ones(1,hsos) 7*ones(1,hgos)...
        8*ones(1,hfos)];


simulationinput = zeros(18,1000);
simulationinput(1:9,:) = horzcat(awaybatting,repmat(homepitching,[9,1]));
simulationinput(10:18,:) = horzcat(homebatting,repmat(awaypitching,[9,1]));

end
