import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.integrate import quad


#
#--------------- Utility functions for Normal Distributions and z Scores ---------------#
#
# Calculate the density (relative frequency) 
# function of the given input data
def calc_normaldist(data, mu, sigma):
    return  ( 1 / (sigma * np.sqrt(2 * np.pi)) *  
             np.exp( -(data - mu)**2 / (2 * sigma**2)) )


# Convert the given data to z scores:
def calc_zscore(value, mu, sigma):
    return np.round( ((value - mu) / sigma) , decimals=2)


# Convert the z score to the actual value of the data
def calc_targetscore(zscore, mu, sigma):
    return (mu + zscore * sigma)


# Tranform z scores into another type of standard scores:
def transform_zscore(zscore, new_mu, new_sigma):
    return (new_mu + zscore*new_sigma)


# Find the appropriate z score that represents the target percentile rank
def find_zscore(target):
    table = zscores_table()
    
    # Default deviation, used to include the optimal
    # number of zscores within a range, so that the
    # minimal deviation from desired density can be found
    deviation = 0.01
    zscore_range = table[(table >= target - deviation) & (table <= target + deviation)]
    zscore = np.abs(zscore_range - target)
    return zscore[zscore == zscore.min()].index


# Calculate the density of z scores (used as the upper/lower bounds of the integration)
def calc_zscore_density(zscore):
    return ( (1 / np.sqrt(2*np.pi)) *
            (np.exp( - (zscore**2) / 2)) )


# Generate a standard z scores table (of a normal distribution)
def zscores_table():
    zscores = np.round(np.arange(-4, 4.01, 0.01), decimals=2)
    table = pd.Series(data=[0 for i in range(zscores.size)],
                      index=zscores)
    
    # Calculate the area under the curve using 
    # integral calculus on the normal curve formula
    for idx in range(zscores.size):
        table.iloc[idx], ignored = np.round(quad(calc_zscore_density, np.NINF,
                                                 table.index[idx]), decimals=6)
    
    return table


# Get a list of present tick values along x axis that includes some specified addtional ticks
def get_xticks(xticks, arr):
    return np.sort(np.concatenate([xticks, arr]))


# Decide the lower and upper bounds along x axis to draw a shaded area;
# Used in conjunction with draw_shaded_normaldist()
def get_shadedx(bins, lower_lim, upper_lim=0, shade_type="inner"):
    
    # Get the area that lies in between 
    # the leftmost and rightmost bounds
    if shade_type == "inner":
        if upper_lim != 0:
            return bins[(bins >= lower_lim) & (bins <= upper_lim)]
        else:
            # The area from a specified lower bound
            # to the rightmost bound of the distribution
            return bins[bins >= lower_lim]

    # Get two areas, one from the leftmost bound to a 
    # specified upper bound, the other from a specified
    # lower bound to the rightmost bound
    elif shade_type == "outer":
        left_shadedx = bins[bins <= lower_lim]
        right_shadedx = bins[bins >= upper_lim]
        return left_shadedx, right_shadedx
    

# Draw a line graph that simulates a normal distribution; 
# a shaded area with specified boundaries is included
def draw_shaded_normaldist(data, mu, sigma, interval, shade_type="inner"):
    fig = plt.figure()
    ax = plt.axes()
    
    # Get the bins (or the x-axis values obtained from 
    # dividing the data into 1000 smaller intervals)
    # so that their corresponding y values can be calculated
    # using the normal distribution formula
    proportions, bins, ignored = ax.hist(data, bins=1000,
                                         facecolor="none", density=True)
    ax.plot(bins, calc_normaldist(bins, mu, sigma), color="orange")
    
    # Include the interval into the x-axis ticks, 
    # increase the comprehensiveness of the graph 
    xticks = get_xticks(ax.get_xticks(), interval)
    ax.xaxis.set_major_locator(plt.FixedLocator(xticks))
    ax.set_xticklabels(labels=xticks, rotation=-90)
    
    # Fill the specified interval with a grey shade area
    if shade_type == "inner":
        shadedx = get_shadedx(bins, interval[0], interval[1], shade_type)
        ax.fill_between(shadedx, calc_normaldist(shadedx, mu, sigma), color="gray")
    elif shade_type == "outer":
        left_shadedx, right_shadedx = get_shadedx(bins, interval[0], interval[1], shade_type)
        color = "lightgray"
        ax.fill_between(left_shadedx, calc_normaldist(left_shadedx, mu, sigma), color=color)
        ax.fill_between(right_shadedx, calc_normaldist(right_shadedx, mu, sigma), color=color)
        
    return fig, ax
