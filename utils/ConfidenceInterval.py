import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import utils.HypothesisTest as HT


# Construct the confidence interval
def confidence_interval(sample_mean, conf_score, std_error):
    interval = np.empty(shape=(2))
    interval[0] = sample_mean - (conf_score * std_error)
    interval[1] = sample_mean + (conf_score * std_error)
    
    return np.round(interval, decimals=2)


# Calculate the appropriate sample size, given that 
# the z score & population standard deviation are known
def sample_size(conf_score, pop_std, limit_range):
    limit = limit_range / 2
    return np.round(( (conf_score * pop_std) / limit )**2, decimals=0)
