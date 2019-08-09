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

def selection(ranked_batch):
    '''
    Sorts a RANKED_BATCH
    @param ranked_batch RANKED_BATCH
    @return A sorted BATCH
    '''
    global log
    sorted_ranked_batch = sorted(ranked_batch, key=lambda t: t[0])[::-1]
    sorted_batch = [i[1] for i in sorted_ranked_batch]

    log['bests'].append(sorted_batch[0][0])
    print(f"[SELECTION] TOP={sorted_batch[0][0]}")
    
    return sorted_batch

def reproduction(batch):
    '''
    Takes in a BATCH, returns a slightly mutated BATCH.
    '''
    toReturn = []
    for i in range(settings.CC_PER_BATCH):
        index = math.floor(min((10*(1/(i+1))), len(batch)-1))
        parent = batch[index]
        toReturn.append(mutateGenetics(parent))
    return toReturn

def mutateGenetics(genetic_info):
    '''
    Takes in a PHENOTYPE, returns a mutated PHENOTYPE
    '''
    return (mutateFunctionBody(genetic_info[0]), mutateRuleString(genetic_info[1]))

def mutateBit(bit):
    '''
    Takes in a bit, returns a mutated bit.
    '''
    if bit == 1:
        return np.random.choice([1, 0], p=[1-settings.MUTATION_CHANCE, settings.MUTATION_CHANCE])
    else:
        return np.random.choice([1, 0], p=[settings.MUTATION_CHANCE, 1-settings.MUTATION_CHANCE])

def mutateRuleString(rule_string):
    '''
    Takes in a RULE_STRING, returns a mutated RULE_STRING
    '''
    toReturn = ""
    for i in rule_string:
        toReturn+=str(mutateBit(int(i)))
    return toReturn

def mutateFunctionBody(function_body):
    '''
    Takes in a FUNCTION_SPACE, returns a mutated FUNCTION SPACE
    '''
    new_function_body = np.zeros(function_body.shape)
    for x in range(function_body.shape[0]):
        for y in range(function_body.shape[1]):
            new_function_body[x,y] = mutateBit(function_body[x,y])
    return new_function_body