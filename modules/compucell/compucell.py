'''
COMPUCELLS
The idea behind the compucell is that a cellular automaton can act as a function. 
It may be provided with a series of bits as an input, which the function acts upon, 
and produces a series of bits as a result.

A compucell has three parts:
-The Input Space: A 1xN Matrix of bits. On the right, it attaches to the Function Space. It is the input.
-The Function Space: A MxN Matrix of bits. Theoretically, this will mutate the output space, depending on the input space.
-The Output Space: A 1xN Matrix of bits. On the left, it attaches to the function space. After X iterations, 
    the input space is regarded as the output of the function.

Here's What it looks like, where A is the input space, B is the function space, and C is the output space.

ABBBBC
ABBBBC
ABBBBC
ABBBBC
ABBBBC

When all of these parts are put together, we call the resultant space the computation space. (Please note that 
sometimes the output space is not distinct from the function space.)
'''
from . import cellular_automata
from ..utility.binary_tools import *
import numpy as np

class compucell():
    '''
    Represents a compucell. Takes an input through the execute function, and returns an output, based on given parameters.
    '''
    def __init__(self, function_space, iterations, ruleset, outputPartOfFunctionSpace = True):
        '''
        @param function_space FUNCTION_SPACE
        @param iterations Number of times to run the CA in each compucell
        @param RULESET_FUNCTION
        @param outputPartOfFunctionSpace A boolean representing whether or not the output space is distinct from the function space.
        '''
        self.function_space = function_space
        self.iterations = iterations
        self.outputPartOfFunctionSpace = outputPartOfFunctionSpace
        self.cellular_automata = cellular_automata.celluarAutomata()
        self.cellular_automata.setRuleset(ruleset)

    def execute(self, input):
        '''
        Runs the compucell.
        @param INPUT_SPACE
        @return OUTPUT_SPACE
        '''
        width = self.function_space.shape[1]
        height = self.function_space.shape[0]

        assert input.shape[0] == height

        if self.outputPartOfFunctionSpace:
            computation_space = np.concatenate((input, self.function_space), axis = 1)
        else:
            output = np.zeros((height, 1))
            computation_space = np.concatenate((input, self.function_space, output), axis = 1)
        
        result = self.cellular_automata.execute(computation_space, self.iterations)[:, -1]
        return result

class compucellEvaluator():
    '''
    Evaluates a compucell. Given a compucell, and a desired function, ranks the compucell's performance on the function.
    
    '''

    def __init__(self, evaluateFunction):
        '''
        @param evaluateFunction The function to evaluate against. The function must take an INPUT_SPACE and return an OUTPUT_SPACE.
        '''
        self.evaluateFunction = evaluateFunction
    
    def evaluate(self, compucell, verbose = False):
        '''
        Evaluates a compucell.
        @param compucell The compucell to evaluate.
        @param verbose Whether or not to print information about each test.
        @return A score from 1 to 0.
        '''
        height = compucell.function_space.shape[0]
        max_int = 2**height

        score = 0
        max_score = max_int*height

        for i in range(max_int):
            input = intToOneDBitArray(i, height)
            output = compucell.execute(input)
            expected_output = self.evaluateFunction(input)

            current_score = 0
            for e, a in zip(expected_output, output):
                if e[0:1] == a:
                    current_score+=1
            score+=current_score

            if verbose:
                print(f"input: {input.tolist()} expected output: {expected_output.tolist()} actual output: {output.tolist()} score: {current_score}")
        
        performance = score/max_score
        return performance
        
