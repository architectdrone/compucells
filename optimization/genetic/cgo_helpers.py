import compucell as cc
import cellular_automata as ca
import numpy as np
import random
import time
import datetime
import math

import cgo_settings

log = {
    'start_time': str(datetime.datetime.now()).replace(" ", "_").replace(":", "-"),
    'function_name': cgo_settings.FUNCTION_NAME,
    'cc_per_batch': cgo_settings.CC_PER_BATCH,
    'function_space_size': cgo_settings.FUNCTION_SPACE_SIZE,
    'iterations': cgo_settings.ITERATIONS,
    'runs': cgo_settings.RUNS,
    'performance_threshold': cgo_settings.PERFORMANCE_THRESHOLD,
    'input_space_size': cgo_settings.INPUT_SPACE_SIZE,
    'mutation_chance': cgo_settings.MUTATION_CHANCE,
    'avgs': [],
    'bests': [],
}

class functionProxy():
    '''
    So that rulesets can be dynamically generated.
    '''
    def __init__(self, rulesetString):
        self.rulesetString = rulesetString
    
    def ruleset(self, tl, tc, tr, cl, _cc, cr, bl, bc, br):
        bit_array = np.array([[tl],[tc],[tr],[cl],[_cc],[cr],[bl],[bc],[br]])
        integer = cc.oneDBitArrayToInt(bit_array)
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
    if cgo_settings.FUNCTION_NAME == 'ADD2':
        input = cc.oneDBitArrayToInt(input_array)
        result = (input+2)%16
        result_array = cc.intToOneDBitArray(result, input_array.shape[0])
        return result_array
    elif cgo_settings.FUNCTION_NAME == 'ADD1':
        input = cc.oneDBitArrayToInt(input_array)
        result = (input+1)%16
        result_array = cc.intToOneDBitArray(result, input_array.shape[0])
        return result_array

def generateInitialBatch():
    '''
    Generates initial batch. Returns a list of tuples. The first element is the function space. The second is a ruleset string.
    '''
    return [(ca.randomSetup(cgo_settings.INPUT_SPACE_SIZE, cgo_settings.FUNCTION_SPACE_SIZE), generateRulesetString(512)) for i in range(cgo_settings.CC_PER_BATCH)]

def performanceEvalulation(batch):
    '''
    Returns a list of tuples. The first element is a float, corresponding to the performance of the CA at the given index in the list. The second is a tuple of genetic info.
    '''
    my_evaluator = cc.compucellEvaluator(evaluationFunction)
    toReturn = []
    for i in batch:
        my_function_proxy = functionProxy(i[1])
        ruleset = my_function_proxy.ruleset
        compucell_to_evaluate = cc.compucell(i[0], cgo_settings.FUNCTION_SPACE_SIZE, ruleset)
        toReturn.append((my_evaluator.evaluate(compucell_to_evaluate), i))

    return toReturn

def selection(batch):
    '''
    Culls below average cells. Returns list of tuples, each of which is the genetic info of the instance
    '''
    global log
    evaluation_results = performanceEvalulation(batch)
    scores_only = [i[0] for i in evaluation_results]
    average_score = sum(scores_only)/len(scores_only)
    survivors = [i for i in evaluation_results if i[0] >= average_score]
    sorted_survivors = sorted(survivors, key=lambda t: t[0])[::-1]
    sorted_survivors_genetic_info_only = [i[1] for i in sorted_survivors]

    log['avgs'].append(average_score)
    log['bests'].append(sorted_survivors[0][0])
    print(f"[SELECTION] AVG={average_score} ELIM={len(evaluation_results)-len(survivors)} TOP={sorted_survivors[0][0]}")
    
    return sorted_survivors_genetic_info_only

def reproduction(batch):
    '''
    Takes in a list of genetic information, returns a slightly mutated list of genetic information.
    '''
    toReturn = []
    for i in range(cgo_settings.CC_PER_BATCH):
        index = math.floor(min((10*(1/(i+1))), len(batch)-1))
        parent = batch[index]
        toReturn.append(mutateGenetics(parent))
    return toReturn

def mutateGenetics(genetic_info):
    return (mutateFunctionBody(genetic_info[0]), mutateRuleString(genetic_info[1]))

def mutateBit(bit):
    if bit == 1:
        return np.random.choice([1, 0], p=[1-cgo_settings.MUTATION_CHANCE, cgo_settings.MUTATION_CHANCE])
    else:
        return np.random.choice([1, 0], p=[cgo_settings.MUTATION_CHANCE, 1-cgo_settings.MUTATION_CHANCE])

def mutateRuleString(rule_string):
    '''
    Mutates a rulestring
    '''
    toReturn = ""
    for i in rule_string:
        toReturn+=str(mutateBit(int(i)))
    return toReturn

def mutateFunctionBody(function_body):
    '''
    Mutates a function body
    '''
    new_function_body = np.zeros(function_body.shape)
    for x in range(function_body.shape[0]):
        for y in range(function_body.shape[1]):
            new_function_body[x,y] = mutateBit(function_body[x,y])
    return new_function_body