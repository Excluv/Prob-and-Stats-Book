import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


# Calculate the mean of each variable distribution
def calc_mean(x, y):
    x = np.array(x)
    y = np.array(y)
    return x.mean(), y.mean()


# Calculate the sum of squares of a variable
def calc_ss(data):
    data = np.array(data)
    return np.sum( (data - data.mean())**2 )


# Calculate the sum of product of variables
def calc_sop(x, y):
    x_mean, y_mean = calc_mean(x, y)
    product = (x - x_mean) * (y - y_mean)
    return np.sum(product)


# Calculate the Pearson r correlation coefficient
def pearson_coefficient(x, y):
    x = np.array(x)
    y = np.array(y)
    
    ss_x = calc_ss(x)
    ss_y = calc_ss(y)
    
    numerator = calc_sop(x, y)
    denominator = np.sqrt(ss_x * ss_y)
    return np.round(numerator / denominator, decimals=2)


# Calculate the Point-biserial correlation coefficient
def pbi_coefficient(p, q, scores):
    p = np.array(p)
    q = np.array(q)
    scores = np.array(scores)

    # Calculate the mean of the group coded as 1
    # and its proportion in the distribution
    p_mean = p.mean()
    p_proportion = np.round(p.size / scores.size, decimals=2)
    
    # Calculate the mean of the group coded as 0
    q_mean = q.mean()
    q_proportion = 1 - p_proportion
    
    proportion = np.sqrt(p_proportion * q_proportion)
    relative_standing = (p_mean - q_mean) / scores.std() # Std of all scores
    return relative_standing * proportion
    

# Draw a scatterplot representing the distribution
def draw_scatterplot(x, y):
    fig = plt.figure()
    ax = plt.axes()
    
    ax.scatter(x, y, s=15, 
               marker='o', 
               c="tab:blue")
               
    return fig, ax