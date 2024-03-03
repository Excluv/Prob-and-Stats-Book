import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import utils.NormalDistribution as ND
import utils.CorrelationCoefficient as CC
from scipy.integrate import quad


#
#--------------- Utility functions for z Test ---------------#
#
# List all possible permutations of random samples (with replacement)
def all_samples(population, sample_size):
    pop_size = population.size
    repetition = 0
    
    dummy = np.empty(shape=(np.power(pop_size, sample_size), sample_size), dtype=np.int8)
    
    # Total number of elements in each column = pop_size ^ sample_size
    # where each element of the population takes exactly 
    # pop_size ^ (sample_size - column_index)
    for i in range(sample_size, 0, -1):
        temp = np.repeat(population, np.power(pop_size, i - 1), axis=0)
        arr = np.repeat([temp], np.power(pop_size, repetition), axis=0).reshape(-1)
        dummy[:, repetition] = arr
        repetition += 1
    
    return dummy
        

# Constuct a distribution of sample means
def sampling_distribution(population, sample_size):
    population = np.array(population)
    
    # Calculate the mean of each permutation of random sample
    args = [population, sample_size]
    means = all_samples(*args).mean(axis=1)
    
    # Find the frequencies of occurrences of sample means
    means, freq = np.unique(means, return_counts=True)
    
    # Actual frequency distribution
    freq_dist = pd.DataFrame(data={"Sample Mean": means,
                                   "Probability": freq / means.size})
    return freq_dist


# Calculate standard error of the mean:
def mean_stderror(pop_std, sample_size):
    return pop_std / np.sqrt(sample_size)


# Convert sample mean to z:
def mean_zscore(pop_mean, pop_std, sample_mean, sample_size):
    deviation = sample_mean - pop_mean
    stderror = mean_stderror(pop_std, sample_size)
    
    return np.round(deviation / stderror, decimals=2)


# Calculate and display the power curves
# Currently applied for one-tailed tests only
def power_curves(hyp_mean, std, sample_size, test_type):
    # Calculate required parameters:
    # true means, standard error and the actual score at (+-1.65 * standard error)
    means_diff = np.linspace(0, 20, 1000)
    true_mean = hyp_mean + means_diff
    standard_error = std / np.sqrt(sample_size)
    critcal_value = 1.65
    target_score = (critcal_value * standard_error) + hyp_mean

    # Calculate the z scores of the target score relatively to the true means
    zscore_error = np.round((target_score - true_mean) / standard_error, decimals=2)
    zscore_error[zscore_error < -4.01] = np.repeat([-4.00], zscore_error[zscore_error < -4.01].size)

    power = list()
    # Calculate the area under the curve according to the obtained z scores
    for zscore in zscore_error:
        boundaries = [np.NINF, zscore]
        error_prob, ignore = np.round(quad(ND.calc_zscore_density, *boundaries),
                                      decimals=4)
        power.append(1 - error_prob)

    # Plot the curve: 
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(means_diff, power, color="black", label=sample_size)
    ax.set_title(label=f"One-tailed Test ({test_type} critical)")

    # Decorate the plot:
    xticks = np.arange(0, 21, 2)
    ax.xaxis.set_major_locator(plt.FixedLocator(xticks))
    ax.set_xlabel("Difference (Effect Size)")
    ax.set_ylabel("Power")
    ax.tick_params(axis="both", direction="in", length=6)
    ax.legend(title="Sample Size", loc="upper left", bbox_to_anchor=(1, 1));
    
    return fig, ax


#
#--------------- Utility functions for t Test ---------------#
#
# Calculate the pooled variance estimate
def pooled_variance(data_set1, data_set2, df):
    ss_1 = CC.calc_ss(data_set1)
    ss_2 = CC.calc_ss(data_set2)
    
    return np.round((ss_1 + ss_2) / df, decimals=4)


# Calculate the estimated standard error for one and two samples t test
def estimated_stderror(data=None, sample_size=None, pearson_r=None, test_type="1 sample"):
    if (test_type == "1 sample") or (test_type == "2 related samples"):
        df = sample_size - 1
        sample_std = np.sqrt(CC.calc_ss(data) / df)
        
        return np.round(sample_std / np.sqrt(sample_size), decimals=2)
    
    if test_type == "2 independent samples":
        variance = pooled_variance(*data, np.sum(sample_size) - 2)
        std_errors = variance / np.array(sample_size)
        
        return np.round(np.sqrt(std_errors.sum()), decimals=2)
    
    if test_type == "correlation coefficient":
        df = sample_size - 2
        corr_variance = 1 - pearson_r**2
        
        return np.round(np.sqrt(corr_variance / df), decimals=2)
    
    
# Calculate the t ratio
def calc_tscore(sample_mean, hyp_mean, est_stderror):
    return np.round((sample_mean - hyp_mean) / est_stderror, decimals=3)
    
    
# Calculate the standardized effect size, Cohen's d
def calc_cohensd(obsv_mean1, obsv_mean2, pooled_variance):
    numerator = obsv_mean1 - obsv_mean2
    denominator = np.sqrt(pooled_variance)
    
    return np.round(numerator / denominator, decimals=2)


#
#--------------- Utility functions for One-Factor F Test ---------------#
#
# Calculate the sum of squares
def calc_ss(data, group_size="equal"):
    data = np.array(data, dtype="object")
    
    if group_size == "equal":
        grand_mean = data.mean()
        group_means = data.mean(axis=1)

        # Calculate the sum of squares between groups
        num_of_group = group_means.size
        ss_between = num_of_group * np.sum( (group_means - grand_mean)**2 )

        # Calculate the sum of squares within groups
        ss_within = np.sum(data**2) - np.sum(data.sum(axis=1)**2) / (data.size / group_means.size)
    
    if group_size == "unequal":
        group_totals = np.array([np.sum(group) for group in data])
        grand_total = group_totals.sum()
        group_sizes = np.array([len(group) for group in data])
        sample_size = group_sizes.sum()
        
        ss_between = np.sum(group_totals**2 / group_sizes) - grand_total**2 / sample_size
        ss_within = np.sum([np.sum(np.square(group)) for group in data]) - np.sum(group_totals**2 / group_sizes)
        
    return np.round(np.array([ss_between, ss_within]), decimals=2)


# Calculate the mean squares
def calc_ms(ss, sample_size, num_of_group):
    df_between = num_of_group - 1
    df_within = sample_size - num_of_group
    df = np.array([df_between, df_within])
    
    return np.roungd(ss / df, decimals=3)


# Calculate the F score
def calc_fscore(ms_between, ms_within):
    return np.round(ms_between / ms_within, decimals=3)


# Calculate the eta squared
def calc_etasquared(ss_between, ss_total):
    return np.round(ss_between / ss_total, decimals=2)


def calc_turkeyshsd(q, ms_within, group_size):
    return np.round(q * np.sqrt(ms_within / group_size), decimals=2)
