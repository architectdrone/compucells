'''
Represents a cellular automata. The scope of this class includes:
-Getting and Setting Rulesets
-Executing Automata with Rulesets
-Returning Information about Rulesets
'''
import numpy as np
import random
import time

class celluarAutomata():
    def __init__(self):
        self.verbose = False
        self.targets = []

    def setRuleset(self, ruleset):
        '''
        Sets the ruleset for the automata. 
        ruleset: A function with eight int inputs, and one int output. The eight inputs correspond to, in order,
            -TOP LEFT
            -TOP CENTER
            -TOP RIGHT
            -LEFT
            -CENTER
            -RIGHT
            -BOTTOM LEFT
            -BOTTOM CENTER
            -BOTTOM RIGHT 
        '''

        self.ruleset = ruleset
    
    def execute(self, positions, iterations, verbose = False):
        myCellular = _cellularAutomataInstance(positions, self.ruleset, targets = self.targets)
        if verbose or self.verbose:
            print(myCellular)
            
        for i in range(iterations):
            myCellular.iterate()
            if verbose or self.verbose:
                print(myCellular)
        return myCellular.positions

class _cellularAutomataInstance():
    '''
    One cellular automata.
    '''

    def __init__(self, startingPositions, ruleset, targets = []):
        '''
        startingPositions: A 2D numpy array of any size, with valid enumerated valued at every position.
        ruleset: See cellularAutomata's setRuleset function
        targets: A list of tuples representing coordinates to highlight. Only makes since if you are printing it.
        '''

        self.positions = startingPositions
        self.ruleset = ruleset
        self.targets = targets
    
    def iterate(self):
        '''
        Perform one CA iteration.
        '''

        width = self.positions.shape[0]
        height = self.positions.shape[1]
        newPositions = np.zeros((width, height))

        for x in range(width):
            for y in range(height):
                tl = self.getPosition(x+1, y+1)
                tc = self.getPosition(x,   y+1)
                tr = self.getPosition(x-1, y+1)
                cl = self.getPosition(x+1, y)
                cc = self.getPosition(x,   y)
                cr = self.getPosition(x-1, y)
                bl = self.getPosition(x+1, y-1)
                bc = self.getPosition(x,   y-1)
                br = self.getPosition(x-1, y-1)
                next_state = self.ruleset(tl, tc, tr, cl, cc, cr, bl, bc, br)
                newPositions[x, y] = next_state
        
        self.positions = newPositions
    
    def getPosition(self, x, y):
        if x < 0:
            return 0
        if x >= self.positions.shape[0]:
            return 0
        if y < 0:
            return 0
        if y >= self.positions.shape[1]:
            return 0
        
        return self.positions[x, y]
    
    def __str__(self):
        NOT_EMPTY = '█'
        EMPTY = '░'
        TARGET = '▒'

        toReturn = ""

        for x in range(self.positions.shape[0]):
            for y in range(self.positions.shape[1]):
                if self.positions[x, y] == 1:
                    toReturn+=NOT_EMPTY
                elif (x, y) in self.targets:
                    toReturn+=TARGET
                else:
                    toReturn+=EMPTY
            toReturn+='\n'
        
        return toReturn

def conway(tl, tc, tr, cl, cc, cr, bl, bc, br):
    numberOfNeighbors = tl+tc+tr+cl+cr+bl+bc+br
    live = cc == 1
    #print(live, numberOfNeighbors)
    if live and numberOfNeighbors < 2:
        #print("Cell is alive, but has less than 2 neighors, so it dies")
        return 0
    elif live and numberOfNeighbors in [2, 3]:
        #print("Cell is alive and well")
        return 1
    elif live and numberOfNeighbors > 3:
        #print("Cell is alive, but has more than 3 neighors, so it dies")
        return 0
    elif not live and numberOfNeighbors == 3:
        #print("Cell is dead, but has three neighbors, so it lives.")
        return 1
    else:
        #print("Cell is dead an stays dead.")
        return 0

def randomSetup(x, y):
    toReturn = np.zeros((x, y))

    for i_x in range(x):
        for i_y in range(y):
            toReturn[i_x, i_y] = random.choice([0, 1])
    
    return toReturn
