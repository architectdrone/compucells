import math
settings = {}

def temperature(k):
    '''
    Takes in a float, returns a temperature (which is also a float.)
    '''

    return settings['INITIAL_TEMPERATURE']*k

def E(k):
    '''
    Converts a score to an energy. Since SA is made to detect minima, high scores -> low energies. Currently, we just do 1-k.
    '''

    return 1-k

def P(e_s, e_s_new, temperature):
    '''
    Returns the probability of jumping to another point.
    '''
    if e_s_new < e_s:
        return 1
    else:
        return math.exp(-(e_s_new-e_s)/temperature)
    return 