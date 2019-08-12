from ...compucell import compucell as cc
from ...compucell import cellular_automata as ca
from ...utility.binary_tools import *
import numpy as np
import random
import time
import datetime
import math

settings = {}
log = {
    'avgs': [],
    'bests': [],
}

def histogram(evaluated_batch):
    '''
    Puts a text based histrogram of scores on the command line.
    '''
    INCREMENTS = 5
    at_each = [0 for _ in range(int(100/INCREMENTS))]
    for i in evaluated_batch:
        score = i[0]
        index = int(math.floor((score*100)/INCREMENTS))
        at_each[index]+=1
    for i, e in enumerate(at_each):
        if e == 0:
            bar = ""
        else:
            bar = "X"*int(((e/10)+1))
        print(f"{i*INCREMENTS}: {bar}")


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
        N = settings['PHENOTYPES_PER_BATCH']-1
        parent1 = batch[burritoBowlMap(i)]
        parent2 = batch[burritoBowlMap(i)+1] #Take the next top performer and mate with it. This forbids incest, which is probably a good thing. (?)
        child = combinePhenotypes(parent1, parent2)
        mutated_child = mutatePhenotype(child)
        toReturn.append(mutated_child)
    return toReturn

def burritoBowlMap(x):
    '''
    This mapping function has two constant parameters: I and P. (Defined as BB_I and BB_P in settings)
    Each parent (sorted from best to worst, with best having index 0) gets either I-P*x or 0 children (whichever is greater).
    (For example, if I is 100, and P is 10, 0 would get 100, 1 would get 90, 2 would get 80 ...)
    The Burrito Bowl function takes in a child and assigns it a parent's index based off of this idea.
    (I arrived at this function after a lot of algebra, so you will have to take my word for it that it works. Also try plotting it on your graphing calculator)

    BB(x) = -(-2I+P+sqrt(4I^2+4PI+P^2-8PX))/2P

    If N is the number of children needing to be assigned, make sure that:

    (4I^2+4PI+P^2)/8P >= N-1 (Preferrably Equal)

    Or not every child will get a parent, which would sad. (Also, the script will crash.)
    '''

    I = settings['BB_I']
    P = settings['BB_P']
    N = settings['PHENOTYPES_PER_BATCH']

    assert ((4*(I**2))+(4*P*I)+P**2)/8*P >= N-1, "Check parameters BB_P and BB_I"
    inside_sqr_root = 4*(I**2)+4*P*I+(P**2)-8*P*x
    BB = -(-2*I+P+math.sqrt(inside_sqr_root))/(2*P)
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

def combinePhenotypes(parent1_phenotype, parent2_phenotype):
    '''
    Takes in two PHENOTYPES and splices them together.
    '''

    return (combineFunctionBodies(parent1_phenotype[0], parent2_phenotype[0]), combineRuleStrings(parent1_phenotype[1], parent2_phenotype[1]))

def combineRuleStrings(parent1_rule_string, parent2_rule_string):
    '''
    Takes in two RULE_STRINGs and splices them together.
    '''

    num_splices = settings['COMBINATION_SPLICES']
    length = len(parent1_rule_string)
    splice_indexes = [random.randrange(0, length) for i in range(num_splices)]

    which_parent = 1
    to_return = ""
    for i in range(length):
        if i in splice_indexes:
            #Switch
            if which_parent == 2:
                which_parent = 1
            else:
                which_parent = 2
        if which_parent == 1:
            to_return+=parent1_rule_string[i]
        else:
            to_return+=parent2_rule_string[i]
    return to_return

def combineFunctionBodies(parent1_function_space, parent2_function_space):
    '''
    Takes in two FUNCTION_SPACEs and splices them together.
    '''

    num_splices = settings['COMBINATION_SPLICES']
    length = parent1_function_space.size
    splice_indexes = [random.randrange(0, length) for i in range(num_splices)]

    current_position = 0
    which_parent = 1
    new_function_space = np.zeros(parent1_function_space.shape)
    for x in range(parent1_function_space.shape[0]):
        for y in range(parent1_function_space.shape[1]):
            current_position+=1
            if current_position in splice_indexes:
                #Switch
                if which_parent == 2:
                    which_parent = 1
                else:
                    which_parent = 2
            if which_parent == 1:
                new_function_space[x,y] = parent1_function_space[x,y]
            else:
                new_function_space[x,y] = parent2_function_space[x,y]
    return new_function_space