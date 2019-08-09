import numpy as np

def oneDBitArrayToInt(bit_array):
    '''
    Takes in a VECTOR_PLANE, returns the corresponding integer.
    (The VECTOR_PLANE is big endian)
    '''
    result = 0
    for i,e in enumerate(bit_array):
        result+=(e[0]*(2**(bit_array.size-i-1)))
    return result

def intToOneDBitArray(my_int, size):
    '''
    Takes in an int, and returns the corresponding VECTOR_PLANE of size size.
    '''
    if my_int > 2**size:
        my_int = my_int%(2**size)
    result_list = [int(char) for char in bin(my_int)[2:]]
    if len(result_list) < size:
        for i in range(size-len(result_list)):
            result_list = [0]+result_list
    result = np.c_[result_list]
    return result