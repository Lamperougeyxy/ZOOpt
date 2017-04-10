import Racos.Test.GymTask.Theano
import theano.tensor as T
import numpy as np
import theano

class Layer(object):
    def __init__(self, in_size, out_size, input_w = None, activation_function=None):
        self.__row = in_size
        self.__column = out_size
        self.__w = theano.shared(np.zeros((in_size, out_size)))
        self.__b = theano.shared(np.zeros((out_size,)))
        self.decode_w(input_w)
        self.__wx_plus_b = 0
        self.__activation_function = activation_function
        self.__outputs = 0

    def cal_output(self, inputs):
        # In this example, self.__b = 0
        self.__wx_plus_b = T.dot(inputs, self.__w) + self.__b
        if self.__activation_function is None:
            self.__outputs = self.__wx_plus_b
        else:
            self.__outputs = self.__activation_function(self.__wx_plus_b)
        return self.__outputs

    # The input x is a vector.This function decompose w into a matrix
    def decode_w(self, w):
        if w is None:
            return
        interval = self.__column
        begin = 0
        output = []
        step = len(w) / interval
        for i in range(step):
            output.append(w[begin: begin + interval])
            begin += interval
        self.__w = theano.shared(np.array(output))
        return

    def get_row(self):
        return self.__row

    def get_column(self):
        return self.__column


class NNModel:
    def __init__(self):
        self.__layers = []
        self.__w_size = 0
        return

    # The input layers is a list, each element is the number of neurons in each layer.
    def construct_nnmodel(self, layers):
        # len(layers) is at least 2, including input layer and output layer
        for i in range(len(layers) - 1):
            self.add_layer(layers[i], layers[i + 1], activation_function=T.nnet.sigmoid)
            self.__w_size += layers[i] * layers[i + 1]

    def add_layer(self, in_size, out_size, input_w = None, activation_function=None):
        new_layer = Layer(in_size, out_size, input_w, activation_function)
        self.__layers.append(new_layer)
        return

    # This function decompose a vector into several vectors.
    def decode_w(self, w):
        # ws means a list of w
        begin = 0
        for i in range(len(self.__layers)):
            length = self.__layers[i].get_row() * self.__layers[i].get_column()
            w_temp = w[begin: begin + length]
            self.__layers[i].decode_w(w_temp)
            begin += length
        return

    # output y from input x
    def cal_output(self, x):
        out = x
        for i in range(len(self.__layers)):
            out = self.__layers[i].cal_output(out)
        return out

    def get_w_size(self):
        return self.__w_size

