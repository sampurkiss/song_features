# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 20:56:43 2019

@author: Sam Purkiss
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cost_and_grad import compute_cost, compute_grad
import clustering_algorithms

billboard_charts_2000_on = pd.read_csv('song_details.csv')

#Show summary stats
for i in billboard_charts_2000_on.columns:
    print(billboard_charts_2000_on[i].describe())

#Put key variables into a vector
keys = []
for i in billboard_charts_2000_on['key'].dropna():
    if i not in keys:
        keys.append(i)
keys.sort()
key_dict = {"0":"C", 
        "1":"C#",
        "2":"D",
        "3":"D#",
        "4":"E",
        "5":"F",
        "6":"F#",
        "7":"G" ,
        "8":"G#",	
        "9":"A",
        "10":'A#,Bb',
        '11':'B'}

#######################################
#Create charts
temp = billboard_charts_2000_on.copy()
temp['extra'] = 1
temp.loc[:,'key'] = temp.loc[:,'key'].map(lambda x: key_dict[str(int(x))])
temp = temp[['year','key','extra']].groupby(by =['year','key']).sum().reset_index()
temp = temp.pivot(index='year',columns = 'key',values = 'extra')
temp = temp.div(temp.sum(axis=1),axis=0)
temp.plot.bar(stacked=True)

temp = billboard_charts_2000_on[['year','energy','danceability','valence']].groupby(by='year').mean()

temp.plot.line()
#fig,ax = plt.subplots()
#ax.plot(billboard_charts_2000_on['WeekID'],billboard_charts_2000_on['key'],marker='.')




#Want to see if I can predict what leads to more time on billboards
#Y: Weeks on billboard
#X: everything else.Inludes music feature and year
#Cleaning: 
#Remove any nas
billboard_charts_2000_on = billboard_charts_2000_on.dropna()
#randomize data
billboard_charts_2000_on = billboard_charts_2000_on.sample(frac=1)

#Step 1: create X and Y
y = np.transpose(np.matrix(billboard_charts_2000_on['Weeks on Chart']))
X = billboard_charts_2000_on[['Peak Position','year', 'danceability', 'energy',
                              'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                              'instrumentalness', 'liveness', 'valence', 'tempo', 
                              'duration_ms', 'time_signature']]
X = np.matrix(X)
X = X[0:1000,:]
y = y[0:1000,:]

name_vector = billboard_charts_2000_on[['Song', 'Performer']]
#Step 2: Generate theta vector
m,features = X.shape
#Normalize all X
mu = sum(X)/m
sigma = sum(np.square(X-mu))/m

X = (X-mu)/sigma
#Generate bias units in X
X = np.append(np.ones([m,1]),X,axis=1)
m,features = X.shape


theta = np.random.randn(1,features)

historic_costs = []
iteration = []
for i in range(1,1000):
    iteration.append(i)
    cost  = compute_cost(X,y, theta, lambda_ = 1)
    grad = compute_grad(X,y, theta, lambda_ = 1)
    historic_costs.append(cost)
    learning_rate = .003
    theta= theta - learning_rate*grad

plt.plot(iteration, historic_costs)

#Step 3: split X into training, CV and test sets. Randomly select from arrays
#or shuffle to avoid data being organized by year

#optipy.minimize((lambda x: compute_cost(X,y,x)), 
#                theta, method = 'BFGS',
#                jac = (lambda x: compute_grad(X,y,x)),
#                options = {'maxiter':1})

#Step 3: generate cost function and run gradient descent


#############################################
#K-means to cluster the data
#############################################
charts = billboard_charts_2000_on[['Song','Performer','track_id',
                              'danceability', 'energy',
                              'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                              'instrumentalness', 'liveness', 'valence', 'tempo', 
                              'time_signature']].reset_index(drop=True).copy()

charts = charts.drop_duplicates()
charts = charts.dropna()
#step 1: define Xs
X = charts[['danceability', 'energy',
                              'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                              'instrumentalness', 'liveness', 'valence', 'tempo', 
                              'time_signature']].copy()
#Because songs show up multiple times, must eliminate duplicates

#Create series of vectors for key
keys = []
for key in X.loc[:,'key']:
    if key not in keys:
        keys.append(key)
keys.sort()

#for key in keys:
#    X.loc[:,key]= X.loc[:,'key'].apply(lambda x: 1 if x==key else 0)
X = X.drop(columns='key')
X = np.matrix(X)



#col2-transform to log
X[:,1]= np.square(X[:,1])

#X = X[0:1000,:]
#Normalize all X
X = clustering_algorithms.normalize_values(X,use_sigma=False)

name_vector = charts

#step 2: define number of clusters and generate starting point
k = 300
#Need to be careful here, had problem where the same number
#was being sampled multiple times
J_list=[]    
centroids, cluster_allocation = clustering_algorithms.initialize_centroids(X, k)  
for i in range(0,50):
    cluster_allocation,centroids = clustering_algorithms.generate_centroids(X,cluster_allocation,k)
    J = clustering_algorithms.k_means_cost(X,centroids,cluster_allocation)
    print(J)
    J_list.append(J)

group = name_vector.loc[cluster_allocation==1]
name_vector.insert(3, 'cluster_grouping', cluster_allocation)
name_vector.to_csv('grouped_songs.csv', index=False)

    
J_list = []    
for k in range(1,200):
    centroids, cluster_allocation = clustering_algorithms.initialize_centroids(X, k) 
    for i in range(0,10):
        cluster_allocation,centroids = clustering_algorithms.generate_centroids(X,cluster_allocation,k)
        J = clustering_algorithms.k_means_cost(X,centroids,cluster_allocation)
    J_list.append(J)

plt.plot(J_list)

#step 3: step through cluster algorithm
#Calculate euclidian distance from each point to centroid
#min||x-mu|| = min sqrt(sum((x-mu)^2))

#assign data points to closest point in cluster_values






