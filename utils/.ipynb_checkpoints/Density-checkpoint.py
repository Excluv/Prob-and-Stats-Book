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


# List all possible permutations of random samples (with replacement)
def all_samples(population, sample_size, idx):
    x, y = np.meshgrid(population, population)
    
    # Reshape x array to merge it with y
    temp = x[:, idx]
    temp = temp[:, np.newaxis]
    
    return np.concatenate([temp, y[:, :(sample_size-1)]], axis=1)
            

# Constuct a distribution of sample means
def sampling_distribution(population, sample_size):
    population = np.array(population)
    
    # Calculate the mean of each permutation of random sample
    args = [population, sample_size]
    means = np.array([all_samples(*args, i).mean(axis=1) 
                      for i in range(population.size)])
    means = means.reshape(population.size**2)
    
    # Find the frequencies of occurrences of sample means
    means, freq = np.unique(means, return_counts=True)
    
    # Actual frequency distribution
    freq_dist = pd.DataFrame(data={"Sample Mean": means,
                                   "Probability": freq/(population.size**2)})
    return freq_dist
