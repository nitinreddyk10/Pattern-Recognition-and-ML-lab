# -*- coding: utf-8 -*-
"""q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19ADst1QBpjw92TeTu9NyImr5vrIaKNRR

QUESTION 2:
Train a single perceptron and SVM to learn the two classes in the following table.

 x1 x2  ω
 2   2   1
-1  -3  0
-1   2   1
 0  -1   0
 1   3   1
-1  -2  0
 1  -2  0
-1  -1  1



where x1 and x2 are the inputs and ω is the target class. Assume that all the weights of the perceptron are initialized as 0 with learning rate 0.01 and 0.5 separately. Also, tabulate the number of iterations required to converge the perception algorithm with these two learning rates.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

d = {'X1':[2, -1, -1, 0, 1, -1, 1, -1], 'X2':[2, -3, 2, -1, 3, -2, -2, -1], 'W':[1, 0, 1, 0, 1, 0, 0, 1]}
df = pd.DataFrame(data = d)
df

"""Training Data"""

X = df.drop('W', axis = 1).to_numpy()
y = np.array(df['W'])

"""Perceptron Training

For Learning Rate 0.01,0.5
"""

# Initialize weights, bias, and learning rates
learning_rates = [0.01, 0.5]
converged_iterations = []

for alpha in learning_rates:
    w = np.zeros(X.shape[1])  # Initialize weights
    b = 0  # Initialize bias
    converged = False
    iters = 0

    while not converged:
        converged = True
        for i in range(len(X)):
            prediction = np.dot(X[i], w) + b
            if (prediction >= 0) and (y[i] == 0):
                w -= alpha * X[i]
                b -= alpha
                converged = False
            elif (prediction < 0) and (y[i] == 1):
                w += alpha * X[i]
                b += alpha
                converged = False
            iters += 1

    converged_iterations.append(iters)

# Print results
for i, alpha in enumerate(learning_rates):
    print(f"Learning Rate = {alpha}, Iterations to Converge = {converged_iterations[i]}")

"""SVM Training"""

# Define learning rate and the number of iterations
learning_rate = 0.23
num_iterations = 100

# Initialize weights and bias
w = np.zeros(X.shape[1])
b = 0

# Define the hinge loss function
def hinge_loss(w, b, X, y):
    loss = 1 - y * (np.dot(X, w) + b)
    return max(0, loss)

# Training the SVM using stochastic gradient descent
for _ in range(num_iterations):
    for i in range(len(X)):
        if y[i] * (np.dot(X[i], w) + b) >= 1:
            w -= learning_rate * (2 * 1/num_iterations * w)
        else:
            w -= learning_rate * (2 * 1/num_iterations * w - np.dot(X[i], y[i]))
            b -= learning_rate * y[i]

# Make predictions
def predict(X, w, b):
    return np.sign(np.dot(X, w) + b)

# Test the model on new data
new_data = np.array([[2, -3], [-2, 0], [0, 0]])
predictions = predict(new_data, w, b)

print("Predictions:", predictions)