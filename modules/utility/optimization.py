import numpy as np
import random 
from .binary_tools import *
from ..compucell import compucell as cc
from ..compucell import cellular_automata as ca

settings = {}

class functionProxy():
    '''
    So that rulesets can be dynamically generated.
    '''
    def __init__(self, rule_string):
        '''
        @param rule_string RULE_STRING
        '''
        self.rule_string = rule_string
    
    def ruleset(self, tl, tc, tr, cl, _cc, cr, bl, bc, br):
        '''
        A RULESET_FUNCTION that corresponds to the given RULE_STRING
        '''
        bit_array = np.array([[tl],[tc],[tr],[cl],[_cc],[cr],[bl],[bc],[br]])
        integer = oneDBitArrayToInt(bit_array)
        return int(self.rule_string[int(integer)])

def generateRulesetString(length):
    '''
    Generates a random RULE_STRING of the given length. This should generlly be 512.
    '''
    toReturn = ""
    for i in range(length):
        toReturn+=(str(random.choice([0,1])))
    return toReturn

def evaluationFunction(input_array):
    '''
    This is a generalized function. Any function body may be provided here, as long as it takes an INPUT_SPACE and returns an OUTPUT_SPACE.
    '''
    if settings['FUNCTION_NAME'] == 'ADD2':
        input = oneDBitArrayToInt(input_array)
        result = (input+2)%16
        result_array = intToOneDBitArray(result, input_array.shape[0])
        return result_array
    elif settings['FUNCTION_NAME'] == 'ADD1':
        input = oneDBitArrayToInt(input_array)
        result = (input+1)%16
        result_array = intToOneDBitArray(result, input_array.shape[0])
        return result_array

def generateInitialBatch():
    '''
    Generates a random BATCH.
    '''
    return [(ca.randomSetup(settings['INPUT_SPACE_SIZE'], settings['FUNCTION_SPACE_SIZE']), generateRulesetString(512)) for i in range(settings['CC_PER_BATCH'])]

def performanceEvalulation(batch):
    '''
    Takes in a BATCH, returns a RANKED_BATCH.
    '''
    my_evaluator = cc.compucellEvaluator(evaluationFunction)
    toReturn = []
    for i in batch:
        my_function_proxy = functionProxy(i[1])
        ruleset = my_function_proxy.ruleset
        compucell_to_evaluate = cc.compucell(i[0], settings['FUNCTION_SPACE_SIZE'], ruleset)
        toReturn.append((my_evaluator.evaluate(compucell_to_evaluate), i))

    return toReturn
