import numpy as np
import pandas as pd

# Calculate factorial expression
def factorial(num):
    if num == 0:
        return 1
    
    return num * factorial(num-1)


# Calculate combinations
def combinations(objects, sample, rep=False):
    match rep:
        case False: # Order does not matter, repetition not allowed
            return ( factorial(objects) / 
                     (factorial(sample) * factorial(objects - sample)) )
        case True: # Order does not matter, repetition allowed
            return ( factorial(objects + sample - 1) /
                     (factorial(sample) * factorial(objects - 1)) )

            
# Calculate permutations          
def permutations(objects, sample, rep=False):
    match rep:
        case False: # Order matters, repetition not allowed
            return combinations(objects, sample) * factorial(objects)
        case True: # Order matters repetition allowed
            return np.power(objects, sample)

