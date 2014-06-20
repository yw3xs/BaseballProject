'''

this file generates the input for BaseballSimulator.  it will read the
excel files in MATLAB Inputs and generate a 20x1000 matrix of outcomes
for each pitcher and hitter.  

'''

import csv

def intlist(num, x):
    '''returns a list of the number num repeated x times'''
    return [num for n in range(x)]

def SimulationInputGeneratorWeightedCurrent(inputfile,abcw,apcw,hbcw,hpcw,pw):

    excelinput = []
    with open(inputfile, 'r') as file:
        for line in csv.reader(file):
            excelinput.append([1000*int(elem) for elem in line])


    abaw = 1 - abcw # away batting career weight
    apaw = 1 - apcw # away pitching away weight
    hbhw = 1 - hbcw # home batting home weight
    hphw = 1 - hpcw # home pitching home weight
    bw = 1 - pw # batting weight

    awaybatting = [[] for row in range(9)]
    awaypitching=[]
    homebatting=[[] for row in range(9)]
    homepitching=[]

    for i in range(9):
    
        awalks = int(round(bw*(abcw*excelinput[i,1]+abaw*excelinput[i,17])))
        asingles = int(round(bw*(abcw*excelinput[i,2]+abaw*excelinput[i,18])))
        adoubles = int(round(bw*(abcw*excelinput[i,3]+abaw*excelinput[i,19])))
        atriples = int(round(bw*(abcw*excelinput[i,4]+abaw*excelinput[i,20])))
        ahrs = int(round(bw*(abcw*excelinput[i,5]+abaw*excelinput[i,21])))
        asos = int(round(bw*(abcw*excelinput[i,6]+abaw*excelinput[i,22])))
        agos = int(round(bw*(abcw*excelinput[i,7]+abaw*excelinput[i,23])))
        afos = int(len(awaybatting[0]) - (awalks + asingles + adoubles + atriples + ahrs \
               + asos + agos))
        awaybatting[i] = intlist(1, awalks) + intlist(2, asingles) + intlist(3, adoubles) + \
                         intlist(4, atriples) + intlist(5, ahrs) + intlist(6, asos) + intlist(7, agos) + \
                         intlist(8, afos)
          
    
        hwalks = int(round(bw*(hbcw*excelinput[10+i,1]+hbhw*excelinput[10+i,9])))
        hsingles = int(round(bw*(hbcw*excelinput[10+i,2]+hbhw*excelinput[10+i,10])))
        hdoubles = int(round(bw*(hbcw*excelinput[10+i,3]+hbhw*excelinput[10+i,11])))
        htriples = int(round(bw*(hbcw*excelinput[10+i,4]+hbhw*excelinput[10+i,12])))
        hhrs = int(round(bw*(hbcw*excelinput[10+i,5]+hbhw*excelinput[10+i,13])))
        hsos = int(round(bw*(hbcw*excelinput[10+i,6]+hbhw*excelinput[10+i,14])))
        hgos = int(round(bw*(hbcw*excelinput[10+i,7]+hbhw*excelinput[10+i,15])))
        hfos = int(len(homebatting[0]) - (hwalks + hsingles + hdoubles + htriples + hhrs \
               + hsos + hgos))
        homebatting[i] = intlist(1, hwalks) + intlist(2, hsingles) + intlist(3, hdoubles) + \
                         intlist(4, htriples) + intlist(5, hhrs) + intlist(6, hsos) + intlist(7, hgos) + \
                         intlist(8, hfos)


    awalks = int(round(pw*(apcw*excelinput[10,1]+apaw*excelinput[10,17])))
    asingles = int(round(pw*(apcw*excelinput[10,2]+apaw*excelinput[10,18])))
    adoubles = int(round(pw*(apcw*excelinput[10,3]+apaw*excelinput[10,19])))
    atriples = int(round(pw*(apcw*excelinput[10,4]+apaw*excelinput[10,20])))
    ahrs = int(round(pw*(apcw*excelinput[10,5]+apaw*excelinput[10,21])))
    asos = int(round(pw*(apcw*excelinput[10,6]+apaw*excelinput[10,22])))
    agos = int(round(pw*(apcw*excelinput[10,7]+apaw*excelinput[10,23])))
    afos = int(len(awaypitching) - (awalks + asingles + adoubles + atriples + ahrs \
           + asos + agos))
    awaypitching = intlist(1, awalks) + intlist(2, asingles) + intlist(3, adoubles) + \
                   intlist(4, atriples) + intlist(5, ahrs) + intlist(6, asos) + intlist(7, agos) + \
                   intlist(8, afos)

    hwalks = int(round(pw*(hpcw*excelinput[20,1]+hphw*excelinput[20,9])))
    hsingles = int(round(pw*(hpcw*excelinput[20,2]+hphw*excelinput[20,10])))
    hdoubles = int(round(pw*(hpcw*excelinput[20,3]+hphw*excelinput[20,11])))
    htriples = int(round(pw*(hpcw*excelinput[20,4]+hphw*excelinput[20,12])))
    hhrs = int(round(pw*(hpcw*excelinput[20,5]+hphw*excelinput[20,13])))
    hsos = int(round(pw*(hpcw*excelinput[20,6]+hphw*excelinput[20,14])))
    hgos = int(round(pw*(hpcw*excelinput[20,7]+hphw*excelinput[20,15])))
    hfos = int(len(homepitching) - (hwalks + hsingles + hdoubles + htriples + hhrs \
            + hsos + hgos)) 

    homepitching = intlist(1, hwalks) + intlist(2, hsingles) + intlist(3, hdoubles) + \
                   intlist(4, htriples) + intlist(5, hhrs) + intlist(6, hsos) + intlist(7, hgos) + \
                   intlist(8, hfos)


    simulationinput = []
    simulationinput(1:9,:) = horzcat(awaybatting,repmat(homepitching,[9,1]));
    simulationinput(10:18,:) = horzcat(homebatting,repmat(awaypitching,[9,1]));

