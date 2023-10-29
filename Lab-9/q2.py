# -*- coding: utf-8 -*-
"""q2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o-akAX3YrSzRHogSD6D2Nlbb9UqBg_Iz

1. Fisherfaces- Face classification using LDA (40 classes)
a) Use the following “face.csv” file to classify the faces of 40 different people using LDA.
b) Do not use the in-built function for implementing LDA.
c) Use appropriate classifier taught in class (any classification algorithm taught in class like Bayes classifier, minimum distance classifier, and so on )
d) Refer to the following link for a description of the dataset:  https://towardsdatascience.com/eigenfaces-face-classification-in-python-7b8d2af3d3ea
"""

#Imports and Dataset Exploration
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from google.colab import drive
drive.mount('/content/drive')

import warnings
warnings.filterwarnings('ignore')

class LDA:
    def __init__(self, n=0):
        self.d1 = n

    def fit(self, X, y):
        self.d = len(X[0])
        self.classes = np.unique(y)
        self.no_of_classes = len(self.classes)
        self.split_X = []
        for c in self.classes:
            class_X = []
            for i in range(len(y)):
                if y[i] == c:
                    class_X.append(X[i])
            self.split_X.append(class_X)
        # print("Split X : ", self.split_X)

        # Step-1: Finding Mean Vectors for each class
        self.mean_vectors = []
        for X_class in self.split_X:
            self.mean_vectors.append(np.mean(X_class, axis=0))
        self.mean_vectors = np.array(self.mean_vectors)

        # Step-2: Computing Scatter Matrices
        # Part-A: Within class Scatter Matrix
        self.covariance_matrices = []
        for X_class in self.split_X:
            self.covariance_matrices.append(np.cov(X_class, rowvar=False))
        self.covariance_matrices = np.array(self.covariance_matrices)
        self.Sw = np.zeros((self.d, self.d))
        for i in range(self.no_of_classes):
            self.Sw += (len(self.split_X[i])-1)*self.covariance_matrices[i]
        # Part-B: Between class Scatter Matrix
        self.overall_mean = np.mean(X, axis=0)
        self.Sb = np.zeros((self.d, self.d))
        for i in range(self.no_of_classes):
            mean_vec = self.mean_vectors[i].reshape(self.d, 1)
            ovr_mean = self.overall_mean.reshape(self.d, 1)
            self.Sb += len(self.split_X[i])*(mean_vec - ovr_mean).dot((mean_vec - ovr_mean).T)

        # Step-3: Finding Eigen Values and Vectors
        self.eig_vals, self.eig_vecs = np.linalg.eig(np.linalg.inv(self.Sw).dot(self.Sb))

        # Step-4: Sorting Eigen Values and deciding on d'
        ind = np.argsort(self.eig_vals)[::-1]
        self.sorted_eig_vals = self.eig_vals[ind]
        self.sorted_eig_vecs = self.eig_vecs[ind]
        if self.d1 < 1:
            if self.d1 <= 0:
                self.d1 = 0.99
            self.total_variance = np.sum(self.sorted_eig_vals)
            self.selected_eig_values = []
            cum_variance = 0
            i = 0
            while cum_variance < self.d1 * self.total_variance:
                cum_variance += self.sorted_eig_vals[i]
                self.selected_eig_values.append(self.sorted_eig_vals[i])
                i += 1
            self.selected_eig_values = np.array(self.selected_eig_values)
            self.d1 = len(self.selected_eig_values)
        self.final_eig_vecs = self.sorted_eig_vecs[:, :self.d1]

    def transform(self, X):
        X1 = np.dot(X, self.final_eig_vecs)
        return X1

def euclidean_distance(X_train, X_test):
    all_point_distances = []
    for i in X_test:
        point_distance = []
        for j in X_train:
            dist = np.sqrt(np.sum((j-i)**2))
            # dist = math.sqrt((j[0] - i[0])**2 + (j[1] - i[1])**2)
            point_distance.append(dist)
        all_point_distances.append(point_distance)
    arr = np.array(all_point_distances)
    return arr

def knn_classify(distance_array, y_train, k):
    array_indexes = []
    for point in distance_array:
        nearest_points = np.argsort(point)[:k]
        array_indexes.append(nearest_points)
    array_indexes = np.array(array_indexes)

    y_values = []
    for point in array_indexes:
        values = []
        for i in point:
            values.append(y_train[i])
        y_values.append(values)
    y_pred = []
    for point in y_values:
        y_pred.append(max(point, key=point.count))
    y_pred = np.array(y_pred)

    return y_pred

def check_accuracy(y_pred, y_test):
    return np.sum(y_pred == y_test)/len(y_test)

path='/content/drive/MyDrive/CS21B2028/PR-ML-Lab/datasets/'
df=pd.read_csv(path+'face.csv')
df

df.shape

df['target'].nunique()

64 * 64

"""Image Visualization"""

def plot_faces(pixels):
    fig, axes = plt.subplots(5, 5, figsize=(6, 6))
    for i, ax in enumerate(axes.flat):
        ax.imshow(np.array(pixels)[i].reshape(64, 64), cmap='gray')
    plt.show()

X = df.drop('target', axis=1)
y = df['target']

plot_faces(X)

"""LDA"""

X_train, X_test, y_train, y_test = train_test_split(X, y)

X_train = X_train.values
X_test = X_test.values
y_train = y_train.values
y_test = y_test.values

print(X_train.shape)

lda = LDA(105)
lda.fit(X_train, y_train)

X_train_lda = lda.transform(X_train)
X_test_lda = lda.transform(X_test)

"""MODEL TRAINING & EVALUATION"""

eud = euclidean_distance(X_train_lda, X_test_lda)
k = 5
y_pred = knn_classify(eud, y_train, k)
print(f"Actual Output: {y_test}\nPredicted Output: {y_pred}")

print(f"Accuracy with k={k} : {check_accuracy(y_pred, y_test)*100}%")