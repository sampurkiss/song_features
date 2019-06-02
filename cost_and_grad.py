# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 19:22:12 2019

@author: Sam Purkiss
"""
import numpy as np


def compute_cost(X, y, theta, lambda_=None):
    """ This function calculates the cost and gradient values
    for a linear function
    Paramaters:
        X: numpy matrix with a bias unit already attached
        y: numpy matrix with y values
        theta: a theta matrix
        lambda_: paramater for regularization, this is optional
    returns:
        value from running cost function
    """
    
    #Set parameters
    J = 0
    #if regularization isn't being used then set
    #lambda to 0
    if lambda_==None:
        lambda_=0
    #Get shape of X to use in cost function
    m,n = X.shape
    
    #Run cost function    
    reg_parameter = (lambda_/m) *np.square(theta[:,1:]).sum()
    J= (1/m)*sum(np.square(X*np.transpose(theta)-y)) +reg_parameter

    return np.float(J)


def compute_grad(X, y, theta, lambda_=None):
    """
    Generate a gradient for theta.
        Paramaters:
        X: numpy matrix with a bias unit already fixed
        y: numpy matrix with y values
        theta: a theta matrix
        lambda_: paramater for regularization, this is optional
    returns:
        Theta shaped gradient vector

    """        
    
    if lambda_==None:
        lambda_=0
    [m,n] = X.shape

    #reshape theta
    theta= np.array(theta)
    theta.shape = (1, n) 
    grad=np.zeros(theta.shape)
    
   
    
    reg_grad = lambda_/m*(theta)
    reg_grad[0] = 0 # don't regularize the bias unit paramater    
    grad = (1/m)*(np.transpose(X)*(X*np.transpose(theta)-y))  + np.transpose(reg_grad)
    grad.shape = theta.shape
    
    return np.array(grad)
