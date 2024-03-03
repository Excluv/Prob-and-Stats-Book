import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import CorrelationCoefficient as CC


# Calculate coefficient term
def calc_slope(x, y):
    r = CC.pearson_coefficient(x, y)
    b = r * np.sqrt(CC.calc_ss(y) / CC.calc_ss(x))
    return b


# Calculate the constant term
def calc_constant(x, y):
    b = calc_slope(x, y)
    x_mean, y_mean = CC.calc_mean(x, y)
    a = y_mean - b * x_mean
    return a

# Calculate the predicted value given an X
def calc_pvalue(x, coefficient, constant):
    return (coefficient * x) + constant


# Calculate the predictable proportion of data
def cacl_r2(x, y):
    r = CC.pearson_coefficient(x, y)
    return r**2


# Calculate the least square regression function
def leastsquares_regression(x, y):
    x = np.array(x)
    y = np.array(y)
    
    coefficient = calc_slope(x, y)
    constant = calc_constant(x, y)
    
    return calc_pvalue(x, coefficient, constant)


# Calculate the standard error of estimate 
def predictive_error(x, y, size, dataset_type: str):
    r = CC.pearson_coefficient(x, y)
    ss_y = CC.calc_ss(y)
    
    if dataset_type == "population":
        s_yx = np.sqrt( (ss_y * (1 - r**2)) / size )
    elif dataset_type == "sample":
        s_yx = np.sqrt( (ss_y * (1 - r**2)) / (size - 2) )
    
    return s_yx


# Visualize the linear regression line
def draw_linregression(x, y):
    function = leastsquares_regression(x, y)
    
    fig, ax = CC.draw_scatterplot(x, y)
    ax.plot(x, function, 
            color="black",
            linestyle="-")
    
    return fig, ax
