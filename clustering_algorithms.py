# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 22:09:55 2019

@author: Sam Purkiss
"""

import numpy as np

def normalize_values(X,use_sigma=True):
    """
    Normalizes the values of X. Can either normalize
    by dividing each feature vector by its respective standard 
    deviation or by the max value in the respective vector.
    Parameters:        
        X: a numpy matrix with dataset of interest
        use_sigma: whether to normalize using sigma
        (True) or by the largest number in the feature 
        vector (False)
    Returns:
        X_normalized: X values normalized based off the 
        decided setting
    """
    
    m,features = X.shape
    mu = sum(X)/m
    if use_sigma:
        sigma = sum(np.square(X-mu))/m
        X_normalized = np.sqrt(np.divide((X-mu),sigma))
    else:
        max_x = np.max(X,axis=0)
        X_normalized = np.divide((X-mu),max_x)
    return X_normalized

def initialize_centroids(X, k):
    """
    Used to select a starting point for centroids. Algorithm
    selects k data points from X and returns the centroid values 
    and location in the index
    paramaters:
        X: a numpy matrix with the dataset of interest
        k: number of centroids to initialize
    Returns:
        centroids, cluster_index
    """
    m,features = X.shape
    initial_centroids = np.random.choice(range(0,m),k,replace=False)
    centroids = X[initial_centroids]
    cluster_index = np.array(range(0,k))
    
    return centroids, cluster_index



def generate_centroids(X, index_location_of_centroids, k):
    """
    Takes existing allocation of centroids and calculates the
    next centroid value. Specifically, it calculates the average
    location of all X values allocated to each centroid, and 
    returns that as the new centroid.
    Parameters:
        X: a numpy index of values
        index_location_of_centroids: an index of values that 
        indicates which centroid each row in X belongs to
        k: number of centroids
        
    Returns:
        cluster_each_x_belongs_to: the updated values 
        for index_location_of_centroids
        new_centroids: the new centroid values
    """

    #initial_centroids should be organized in order of cluster it belongs to
    #eg centroid 0 should correspond to initial_centroids[0]
    
    #Generate variables:
    [m,features] = X.shape
    cluster_each_x_belongs_to =np.array([],dtype='int')
    new_centroids = np.zeros((k,features))
    
    for i in range(0,k):
        #get average location of each cluster
        new_centroids[i,:] = X[np.where(index_location_of_centroids==i),:].mean(axis=1)

    #Generate index value corresponding to the new centroid value
    for row in X:
        distance = np.sum(np.square(row-new_centroids),axis =1)
        #Get the index value of that closest value
        cluster = distance.argmin()
        #Take min distance and assign X value to that cluster
        cluster_each_x_belongs_to = np.append(cluster_each_x_belongs_to,cluster)

        
    return cluster_each_x_belongs_to, new_centroids


def k_means_cost(X,centroid_values,centroid_index_locations):
    
    m,features = X.shape
    J = 1/m*np.square(X-centroid_values[centroid_index_locations]).sum()
    
    return J