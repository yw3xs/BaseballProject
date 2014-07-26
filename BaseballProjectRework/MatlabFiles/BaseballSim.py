'''

this file will simulate baseball games based on player stats

this was originally a matlab script, but is in the process of
being converted.  the file for generating inputs is still in
being converted as well, so neither file has been debugged or
checked for consistency with the original matlab results

'''

import random, sys
from pymongo import Connection
import numpy as np
from createHitterInputValues import *
from createPitcherInputValues import *
from getGameInfo import *

## base scenarios
# 1 = bases empty
# 2 = runner on 1st
# 3 = runner on 2nd
# 4 = runner on 3rd
# 5 = runner on 1st, 2nd
# 6 = runner on 1st, 3rd
# 7 = runner on 2nd, 3rd
# 8 = bases loaded

## batting outcomes
# 1 = walk
# 2 = single
# 3 = double
# 4 = triple
# 5 = homerun
# 6 = strike out
# 7 = ground out
# 8 = fly out


## make matrices
# the row numbers of the following matrices will correspond to the base scenarios
# outlined above, and the column numbers will correspond to the batting
# outcomes


outsAdder = np.array([[0, 0, 0, 0, 0, 1, 1, 1],
	             [0, 0, 0, 0, 0, 1, 2, 1],
	             [0, 0, 0, 0, 0, 1, 1, 1],
	             [0, 0, 0, 0, 0, 1, 1, 1],
	             [0, 0, 0, 0, 0, 1, 2, 1],
	             [0, 0, 0, 0, 0, 1, 2, 1],
	             [0, 0, 0, 0, 0, 1, 1, 1],
	             [0, 0, 0, 0, 0, 1, 2, 1]])
         
baseStateMatrix = np.array([[1, 1, 2, 3, 0, 0, 0, 0],
	                   [4, 6, 2, 3, 0, 1, 0, 1],
	                   [4, 1, 2, 3, 0, 2, 2, 2],
	                   [5, 1, 2, 3, 0, 3, 3, 0],
	                   [7, 4, 2, 3, 0, 4, 3, 4],
	                   [7, 4, 2, 3, 0, 5, 0, 1],
	                   [7, 1, 2, 3, 0, 6, 6, 2],
	                   [7, 4, 2, 3, 0, 7, 6, 4]])
         
runsAdder = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
	             [0, 0, 1, 1, 2, 0, 0, 0],
	             [0, 1, 1, 1, 2, 0, 0, 0],
	             [0, 1, 1, 1, 2, 0, 0, 1],
	             [0, 1, 2, 2, 3, 0, 0, 0],
	             [0, 1, 2, 2, 3, 0, 1, 1],
	             [0, 2, 2, 2, 3, 0, 0, 1],
	             [1, 2, 3, 3, 4, 0, 0, 1]])
    
             
abcw, apcw, hbcw, hpcw, pw = np.array([.5, .5, .5, .5, .5])
abaw, apaw, hbhw, hphw, hw = 1 - np.array([abcw, apcw, hbcw, hpcw, pw])

def get_stuff(box_dict):

	home_hitters, away_hitters = get_hitters(box_dict)
	home_pitcher, away_pitcher = get_pitchers(box_dict)
	winner = get_winner(box_dict)
	
	return home_hitters, away_hitters, home_pitcher, away_pitcher, winner
	
def convert_to_outcome_list(hitter_final):
	
	indexed_hitter = np.zeros([9,1000])
	for i in range(9):
		hitter = hitter_final[i,:]
		indices = [0]
		indices.extend([int(1000*percent) for percent in hitter.cumsum()])
		indices[-1] = 1000 # in case of rounding errors
		for j in range(len(indices)-1):
			indexed_hitter[i,indices[j]:(indices[j]+indices[j+1])] = j
			
	return indexed_hitter

def create_sim_input(home_hitters, away_hitters, home_pitcher, away_pitcher, current_year):

	hh_intermediate = np.zeros([9,8])
	hp_intermediate = np.zeros([9,1])
	ah_intermediate = np.zeros([9,8])
	ap_intermediate = np.zeros([9,1])
	
	for i in range(len(home_hitters)):
		stats = get_hitter(home_hitters[i], current_year, 'Home')
		proj_stats = project_hitter(stats)
		hh_intermediate[i,:] = hbcw*proj_stats[:8] + hbhw*proj_stats[8:]
	
	for i in range(len(away_hitters)):
		stats = get_hitter(away_hitters[i], current_year, 'Away')
		proj_stats = project_hitter(stats)
		ah_intermediate[i,:] = abcw*proj_stats[:8] + abaw*proj_stats[8:]
		
	hp_stats = get_pitcher(home_pitcher, current_year, 'Home')
	proj_hp = project_pitcher(hp_stats)
	hp_intermediate = hpcw*proj_hp[:8] + hphw*proj_hp[8:]

	ap_stats = get_pitcher(away_pitcher, current_year, 'Away')
	proj_ap = project_pitcher(ap_stats)
	ap_intermediate = apcw*proj_hp[:8] + apaw*proj_hp[8:]
	
	hh_final = hw*hh_intermediate + pw*np.tile(ap_intermediate, (9,1))
	ah_final = hw*ah_intermediate + pw*np.tile(hp_intermediate, (9,1))
	
	home_input = convert_to_outcome_list(hh_final)
	away_input = convert_to_outcome_list(ah_final)
	
	return home_input, away_input
	


	
		

## need to convert arrays containing stat percentages to arrays containing
## integers from 1 to 8 (or 0 to 7).  this allows for determination of outcome
## by looking up a value of an index instead of using multiple comparison 
## operators for all of the numGames*atBats outcomes


def simulate(home_input, away_input):
	numGames = 100000 # the number of times to simulate a given game
	atBats = 300; # max number of at bats a team can have in a game without
		          # returning an error in the simulation

	# input_length = length of arrays specified above
	input_length = np.size(home_input,1)
		          
	outcomesA = np.random.randint(0,input_length,size=(numGames*atBats,1)) # random list of indices corresponding to outcomes
	outcomesAIndex = 1
	outcomesH = np.random.randint(0,input_length,size=(numGames*atBats,1))
	outcomesHIndex = 1
	runsA = np.zeros((1,numGames))
	runsH = np.zeros((1,numGames))

	## must generate simulationInput still - it will consist of an average of
	## the hitters and the opposing teams pitcher, can make one for home and one
	## for away

	for i in range(numGames):
		inningNum = 1
		baseState = 0
		outs = 0
		batterA = 0 # index in an array
		batterH = 0 # index in an array
		while (inningNum < 10 or runsA[0,i] == runsH[0,i]):
		    while outs < 3:
		        battingOutcome = away_input[batterA,outcomesA[outcomesAIndex]]
		        outs += outsAdder[baseState,int(battingOutcome)]
		        if outs < 3:
		            runsA[0,i] += runsAdder[baseState,int(battingOutcome)]
		            baseState = baseStateMatrix[baseState,int(battingOutcome)]
		        
		        batterA += 1
		        if batterA == 9:
		            batterA = 0
		        
		        outcomesAIndex += 1
		    
		    outs = 0
		    baseState = 0
		    while outs < 3:
		        battingOutcome = home_input[batterH,outcomesH[outcomesHIndex]]
		        outs += outsAdder[baseState,int(battingOutcome)]
		        if outs < 3:
		            runsH[0,i] += runsAdder[baseState,int(battingOutcome)]
		            baseState = baseStateMatrix[baseState,int(battingOutcome)]
		        
		        batterH += 1
		        if batterH == 9:
		            batterH = 0
		        
		        outcomesHIndex += 1
		    
		    outs = 0
		    baseState = 1
		    inningNum += 1 

	return runsA, runsH


def main():

	box_db = c.BoxScores
	box_dict = box_db.BoxScores2011.find_one()
	home_hitters, away_hitters, home_pitcher, away_pitcher, winner = get_stuff(box_dict)
	home_input, away_input = create_sim_input(home_hitters, away_hitters, home_pitcher, away_pitcher, 2011)
	ra, rh = simulate(home_input, away_input)
	return ra, rh
	
if __name__ == '__main__':
	ra, rh = main()


