import pandas as pd

# this function is called whenever the `ergo train <project> --dataset file.csv`
# command is executed, the first argument is the dataset and it must return
# a pandas.DataFrame object.
def prepare_dataset(filename):
    # simply read as csv
    return pd.read_csv(filename, sep = ',', header = None)

# called during `ergo serve <project>` for each `x` input parameter, use this 
# function to convert, for instance, a file name in a vector of scalars for 
# your model input layer.
def prepare_input(x):
    # simply read as csv
    return pd.read_csv( pd.compat.StringIO(x), sep = ',', header = None)