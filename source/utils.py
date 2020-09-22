import numpy as np
from numpy.linalg import norm
import tensorflow as tf
from tensorflow.keras import layers, Sequential
from typing import List


def create_model(input_dim,
                 embedding_dim,
                 context_dim,
                 output_dim):
    model = Sequential()
    model.add(layers.Embedding(input_dim=input_dim, output_dim=embedding_dim))
    model.add(layers.SimpleRNN(context_dim))
    model.add(layers.Dense(output_dim, activation='sigmoid'))
    optimizer = tf.keras.optimizers.SGD()
    loss_object = tf.keras.losses.CosineSimilarity()
    model.compile(loss="cosine_similarity", optimizer=optimizer)
    return model, optimizer, loss_object


def create_deep_model(input_dim,
                      hidden_dim,
                      n_hidden,
                      output_dim):
    model = DeepModel(input_dim=input_dim, hidden_dim=hidden_dim, n_hidden=n_hidden, output_dim=output_dim)
    optimizer = tf.keras.optimizers.Adam()
    # cosine similarity since that is also the function we use to retrieve the chars
    # from the model output.
    loss_object = tf.keras.losses.CosineSimilarity()
    model.compile(loss="cosine_similarity", optimizer=optimizer)
    model.build(input_shape=input_dim)
    return model, optimizer, loss_object


def create_lstm_model(input_dim,
                      embedding_dim,
                      context_dim,
                      output_dim):
    model = Sequential()
    model.add(layers.Embedding(input_dim=input_dim, output_dim=embedding_dim))
    model.add(layers.SimpleRNN(context_dim))
    model.add(layers.Dense(output_dim, activation='sigmoid'))
    optimizer = tf.keras.optimizers.Adam()
    loss_object = tf.keras.losses.CosineSimilarity()
    model.compile(loss="cosine_similarity", optimizer=optimizer)
    return model, optimizer, loss_object


class DeepModel(tf.keras.Model):
    """
    Deep feedforward network. We agglutinate all character vectors at one position
    into a single vector and then feed that into 2 fully connected layers (so technically
    there is only one real 'deep' layer.
    """
    def __init__(self, input_dim, hidden_dim, n_hidden, output_dim):
        super(DeepModel, self).__init__()
        # project into a single vector
        self.flatten = layers.Flatten(input_shape=input_dim)
        # create as many hidden layers as specified & append them to an internal list
        self.dense_layers = []
        for _ in range(n_hidden):
            self.dense_layers.append(layers.Dense(hidden_dim, activation='relu'))
        # we chose sigmoid as the activation function since the desired output is a multi-
        # hot vector (or a one-hot vector in the case of char embeddings)
        self.out = layers.Dense(output_dim, activation='sigmoid')

    def call(self, inputs, **kwargs):
        # projection
        x = self.flatten(inputs)
        # apply fully connected layers
        for dl in self.dense_layers:
            x = dl(x)
        return self.out(x)


def cos_sim(x: np.array, y: np.array):
    return np.dot(x, y) / (norm(x) * norm(y))


def list_to_str(lst: List[float]):
    s = ""
    for num in lst:
        s += str(int(num)) + ","
    return s[:len(s)-1]


