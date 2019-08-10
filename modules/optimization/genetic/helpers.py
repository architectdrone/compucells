from ...compucell import compucell as cc
from ...compucell import cellular_automata as ca
from ...utility.binary_tools import *
import numpy as np
import random
import time
import datetime
import math

#from . import settings
settings = {}
log = {
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

    log['bests'].append(sorted_ranked_batch[0][0])
    print(f"[SELECTION] TOP={sorted_ranked_batch[0][0]}")
    
    return sorted_batch

def reproduction(batch):
    '''
    Takes in a BATCH, returns a slightly mutated BATCH.
    Top performers should be at the front of the batch.
    '''
    toReturn = []
    toReturn.append(batch[0]) #Elitism
    for i in range(settings['PHENOTYPES_PER_BATCH']-1):
        index = burritoBowlMap(i)
        parent = batch[index]
        toReturn.append(mutatePhenotype(parent))
    return toReturn

def burritoBowlMap(x):
    '''
    This mapping function has two constant parameters: I and P. (Defined as BB_I and BB_P in settings)
    Each parent (sorted from best to worst, with best having index 0) gets either I-P*x or 0 children (whichever is greater).
    (For example, if I is 100, and P is 10, 0 would get 100, 1 would get 90, 2 would get 80 ...)
    The Burrito Bowl function takes in a child and assigns it a parent's index based off of this idea.
    (I arrived at this function after a lot of algebra, so you will have to take my word for it that it works. Also try plotting it on your graphing calculator)

    BB(x) = -(-2I+P-sqrt(4I^2+4PI+P^2-8PX))/2P

    If N is the number of children needing to be assigned, make sure that:

    (4I^2+4PI+P^2)/8P >= N-1 (Preferrably Equal)

    Or not every child will get a parent, which would sad. (Also, the script will crash.)
    '''

    I = settings['BB_I']
    P = settings['BB_P']
    N = settings['PHENOTYPES_PER_BATCH']

    assert ((4*(I**2))+(4*P*I)+P**2)/8*P >= N-1, "Check parameters BB_P and BB_I"
    inside_sqr_root = 4*(I**2)+4*P*I+(P**2)-8*P*x
    BB = -(2*I+P+math.sqrt(inside_sqr_root))/(2*P)
    return math.ceil(BB)

def mutatePhenotype(genetic_info):
    '''
    Takes in a PHENOTYPE, returns a mutated PHENOTYPE
    '''
    return (mutateFunctionBody(genetic_info[0]), mutateRuleString(genetic_info[1]))

def mutateBit(bit):
    '''
    Takes in a bit, returns a mutated bit.
    '''
    if bit == 1:
        return np.random.choice([1, 0], p=[1-settings['MUTATION_CHANCE'], settings['MUTATION_CHANCE']])
    else:
        return np.random.choice([1, 0], p=[settings['MUTATION_CHANCE'], 1-settings['MUTATION_CHANCE']])

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