%% base scenarios
% 1 = bases empty
% 2 = runner on 1st
% 3 = runner on 2nd
% 4 = runner on 3rd
% 5 = runner on 1st, 2nd
% 6 = runner on 1st, 3rd
% 7 = runner on 2nd, 3rd
% 8 = bases loaded
%% batting outcomes
% 1 = walk
% 2 = single
% 3 = double
% 4 = triple
% 5 = homerun
% 6 = strike out
% 7 = ground out
% 8 = fly out
%% make matrices
% the row numbers of the following matrices will correspond to the base scenarios
% outlined above, and the column numbers will correspond to the batting
% outcomes

outsAdder = [0 0 0 0 0 1 1 1;
             0 0 0 0 0 1 2 1;
             0 0 0 0 0 1 1 1;
             0 0 0 0 0 1 1 1;
             0 0 0 0 0 1 2 1;
             0 0 0 0 0 1 2 1;
             0 0 0 0 0 1 1 1;
             0 0 0 0 0 1 2 1];
         
baseStateMatrix = [2 2 3 4 1 1 1 1;
                   5 7 3 4 1 2 1 2;
                   5 2 3 4 1 3 3 3;
                   6 2 3 4 1 4 4 1;
                   8 5 3 4 1 5 4 5;
                   8 5 3 4 1 6 1 2;
                   8 2 3 4 1 7 7 3;
                   8 5 3 4 1 8 7 5];
         
runsAdder = [0 0 0 0 0 0 0 0;
             0 0 1 1 2 0 0 0;
             0 1 1 1 2 0 0 0;
             0 1 1 1 2 0 0 1;
             0 1 2 2 3 0 0 0;
             0 1 2 2 3 0 1 1;
             0 2 2 2 3 0 0 1;
             1 2 3 3 4 0 0 1];
         
%% inialize parameters and random numbers

numGames = 100000; % the number of times to simulate a given game
atBats = 300; % max number of at bats a team can have in a game without
              % returning an error in the simulation
outcomesA = randi(length(simulationInput),[1,atBats*numGames]);
outcomesAIndex = 1;
outcomesH = randi(length(simulationInput),[1,atBats*numGames]);
outcomesHIndex = 1;
runsA = zeros(1,numGames);
runsH = zeros(1,numGames);
  
%% simulate

for i = 1:numGames 
    inningNum = 1;
    baseState = 1;
    outs = 0;
    batterA = 1;
    batterH = 1;
    while inningNum < 10 || runsA(i) == runsH(i)
        while outs < 3
            battingOutcome = simulationInput(batterA,outcomesA(outcomesAIndex));
            outs = outs + outsAdder(baseState,battingOutcome);
            if outs ~= 3
                runsA(i) = runsA(i) + runsAdder(baseState,battingOutcome);
                baseState = baseStateMatrix(baseState,battingOutcome);
            end
            batterA = batterA + 1;
            if batterA == 10
                batterA = 1;
            end
            outcomesAIndex = outcomesAIndex + 1;
        end
        outs = 0;
        baseState = 1;
        while outs < 3
            battingOutcome = simulationInput(9 + batterH,outcomesH(outcomesHIndex));
            outs = outs + outsAdder(baseState,battingOutcome);
            if outs ~= 3
                runsH(i) = runsH(i) + runsAdder(baseState,battingOutcome);
                baseState = baseStateMatrix(baseState,battingOutcome);
            end
            batterH = batterH + 1;
            if batterH == 10
                batterH = 1;
            end
            outcomesHIndex = outcomesHIndex + 1;
        end
        outs = 0;
        baseState = 1;
        inningNum = inningNum + 1; 
    end  
end


difference=runsH-runsA;
hdom=min(difference):max(difference);
h=hist(difference,hdom);