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
    def __init__(self, rulesetString):
        self.rulesetString = rulesetString
    
    def ruleset(self, tl, tc, tr, cl, _cc, cr, bl, bc, br):
        bit_array = np.array([[tl],[tc],[tr],[cl],[_cc],[cr],[bl],[bc],[br]])
        integer = oneDBitArrayToInt(bit_array)
        return int(self.rulesetString[int(integer)])

def generateRulesetString(length):
    toReturn = ""
    for i in range(length):
        toReturn+=(str(random.choice([0,1])))
    return toReturn

def evaluationFunction(input_array):
    '''
    This is a generalized function. Any function body may be provided here, as long as it conforms to the rules.
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
    Generates initial batch. Returns a list of tuples. The first element is the function space. The second is a ruleset string.
    '''
    return [(ca.randomSetup(settings['INPUT_SPACE_SIZE'], settings['FUNCTION_SPACE_SIZE']), generateRulesetString(512)) for i in range(settings['CC_PER_BATCH'])]

def performanceEvalulation(batch):
    '''
    Returns a list of tuples. The first element is a float, corresponding to the performance of the CA at the given index in the list. The second is a tuple of genetic info.
    '''
    my_evaluator = cc.compucellEvaluator(evaluationFunction)
    toReturn = []
    for i in batch:
        my_function_proxy = functionProxy(i[1])
        ruleset = my_function_proxy.ruleset
        compucell_to_evaluate = cc.compucell(i[0], settings['FUNCTION_SPACE_SIZE'], ruleset)
        toReturn.append((my_evaluator.evaluate(compucell_to_evaluate), i))

    return toReturn
