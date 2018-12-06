import logging as log

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout

# build the model
def build_model(is_train):  
    n_inputs       = 517
    n_classes      = 3
    n_hidden       = (600, 600,)
    dropout        = 0.2
    activation     = 'relu'
    out_activation = 'softmax'
  
    model = Sequential()
    for i, n_neurons in enumerate(n_hidden):
        # setup the input layer
        if i == 0:
            model.add(Dense(n_neurons, input_shape = (n_inputs,), activation = activation))
        else:
            model.add(Dense(n_neurons, activation = activation))
        # add dropout
        if is_train:
            model.add(Dropout(dropout))
    # setup output layer
    model.add(Dense(n_classes, activation = out_activation))
    
    return model
