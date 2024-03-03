import numpy as np


# Resolve raw strings of data, designed particularly for solving
# Statistics Book problems
def to_data(data_str: str, ncol=1, name_maxlength=1):
    
    # Each dataset will come in as a list of strings, each element
    # in the list represents a row of the original set
    classes = np.zeros(shape=(len(data_str), ), dtype="object")
    columns = np.zeros(shape=(len(data_str), ncol), dtype="float")
    
    idx = 0
    for string in data_str:
        
        # Each row is split because it contains both the name 
        # of the class and the associated data
        string = string.split()
        
        # In case there's no record of class in the distribution
        if name_maxlength == 0:
            for i in range(ncol):
                columns[idx][i] = string[i]
                
            idx += 1
            continue
        
        # Sometimes the class name contains more than one word
        # so that it needs checking
        if len(string) == (name_maxlength + ncol):
            classes[idx] = " ".join(string[:name_maxlength])
            for i in range(ncol):
                columns[idx][i] = string[i + name_maxlength]
        else:
            classes[idx] = string[0]
            for i in range(ncol):
                columns[idx][i] = string[1 + i]
        
        idx += 1
        
    return classes, columns
    