import itertools

def cruncher(to_crunch):
    '''
    Takes in a list of bit strings, returns a list of bit strings with don't cares highlighted
    '''
    crunched_strings = []
    for i in itertools.combinations(to_crunch, 2):
        a = i[0]
        b = i[1]
        xored = [a_i == b_i for a_i, b_i in zip(a, b)]
        if xored.count(False) == 1:
            index_of_flip = xored.index(False)
            to_append = list(a)
            to_append[index_of_flip] = 'x'
            to_append_string = ''.join(to_append)
            if to_append_string not in crunched_strings:
                crunched_strings.append(to_append_string)
    
    return crunched_strings

def superCrunch(to_crunch):
    '''
    Gets a list of don't cares, and removes all bit strings that are redundant.
    '''
    iterations = [to_crunch]
    for i in range(len(to_crunch[0])-1):
        iterations.append(cruncher(iterations[-1]))
    
    all_iterations = [item for sublist in iterations for item in sublist][::-1]
    to_remove = []
    for tup in itertools.combinations(all_iterations, 2):
        greater_rank = tup[0]
        lower_rank = tup[1]
        differs = False
        for a, b in zip(greater_rank, lower_rank):
            if a == 'x' and b != 'x': #Either smaller is a subset of greater, or they are different.
                continue
            elif a == 'x' and b == 'x': #Same set
                continue
            elif a != b: #Difference
                differs = True
        
        if not differs:
            to_remove.append(lower_rank)
    
    for i in list(set(to_remove)):
        all_iterations.remove(i)
    
    return all_iterations
