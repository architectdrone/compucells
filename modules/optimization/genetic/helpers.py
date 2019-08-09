from ...compucell import compucell as cc
from ...compucell import cellular_automata as ca
from ...utility.binary_tools import *
import numpy as np
import random
import time
import datetime
import math

from . import settings

log = {
    'start_time': str(datetime.datetime.now()).replace(" ", "_").replace(":", "-"),
    'function_name': settings.FUNCTION_NAME,
    'cc_per_batch': settings.CC_PER_BATCH,
    'function_space_size': settings.FUNCTION_SPACE_SIZE,
    'iterations': settings.ITERATIONS,
    'runs': settings.RUNS,
    'performance_threshold': settings.PERFORMANCE_THRESHOLD,
    'input_space_size': settings.INPUT_SPACE_SIZE,
    'mutation_chance': settings.MUTATION_CHANCE,
    'avgs': [],
    'bests': [],
}

def selection(evaluated_batch):
    '''
    Takes a list of tuples. The first element of each is some (float) score. The second element is the phenotype.
    Culls below average cells. Returns list of tuples, each of which is the genetic info of the instance
    '''
    global log
    scores_only = [i[0] for i in evaluated_batch]
    average_score = sum(scores_only)/len(scores_only)
    survivors = [i for i in evaluated_batch if i[0] >= average_score]
    sorted_survivors = sorted(survivors, key=lambda t: t[0])[::-1]
    sorted_survivors_genetic_info_only = [i[1] for i in sorted_survivors]

    log['avgs'].append(average_score)
    log['bests'].append(sorted_survivors[0][0])
    print(f"[SELECTION] AVG={average_score} ELIM={len(evaluated_batch)-len(survivors)} TOP={sorted_survivors[0][0]}")
    
    return sorted_survivors_genetic_info_only

def reproduction(batch):
    '''
    Takes in a list of genetic information, returns a slightly mutated list of genetic information.
    '''
    toReturn = []
    for i in range(settings.CC_PER_BATCH):
        index = math.floor(min((10*(1/(i+1))), len(batch)-1))
        parent = batch[index]
        toReturn.append(mutateGenetics(parent))
    return toReturn

def mutateGenetics(genetic_info):
    return (mutateFunctionBody(genetic_info[0]), mutateRuleString(genetic_info[1]))

def mutateBit(bit):
    if bit == 1:
        return np.random.choice([1, 0], p=[1-settings.MUTATION_CHANCE, settings.MUTATION_CHANCE])
    else:
        return np.random.choice([1, 0], p=[settings.MUTATION_CHANCE, 1-settings.MUTATION_CHANCE])

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