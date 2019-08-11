import copy
import numpy as np

def getNeighbors(phenotype):
    '''
    Takes in a PHENOTYPE, returns a BATCH of PHENOTYPEs that differ by 1 bit from this phenotype.
    '''
    function_space_neighbors = [(i, phenotype[1]) for i in getFunctionBodyNeighbors(phenotype[0])]
    rule_string_neighbors = [(phenotype[0], i) for i in getRuleStringNeighbors(phenotype[1])]
    return rule_string_neighbors+function_space_neighbors

def getRuleStringNeighbors(rule_string):
    '''
    Takes in a RULE STRING, returns a list of rulestrings that differ by one bit.
    '''

    to_return = []
    for i, e in enumerate(rule_string):
        oppBit = ""
        if e == '1':
            oppBit = '0'
        else:
            oppBit = '1'
        to_return.append(rule_string[:(i-1)]+oppBit+rule_string[i:])
    
    return to_return

def getFunctionBodyNeighbors(function_space):
    '''
    Returns a list of neighboring function spaces.
    '''

    to_return = []
    for x in range(function_space.shape[0]):
        for y in range(function_space.shape[1]):
            oppBit = 0
            if function_space[x, y] == 0:
                oppBit = 1
            else:
                oppBit = 0
            new_function_space = copy.copy(function_space)
            new_function_space[x, y] = oppBit
            to_return.append(new_function_space)
    return to_return