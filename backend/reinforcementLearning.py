## IMPORTS
import seaborn as sb
import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from sklearn_extra.cluster import KMedoids
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.preprocessing import StandardScaler
import random

OG_FEATURES = None
ALGORITHMS = None
NUM_ALG = None
FEATURES = None

##### ALGORITHMS #####
"""
Performs KMeans clustering using the data from selected_features.
If mode = 0, the silhouette score of the clustering is returned.
If mode = 1, the labels of the clustering is returned.
"""
def kmeans_clustering(selected_features,mode, n_clusters=2, max_iter=300):
    """
    Perform KMeans clustering on the input samples
    
    Parameters:
        samples: array-like, shape (n_samples, n_features)
        n_clusters: int, number of clusters (default=2)
        max_iter: int, maximum iterations (default=300)
    
    Returns:
        silhouette_coef: silhouette coefficient score
    """
    # Filter the selected features
    X = selected_features
    
    # Standardize selected features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    best_k = n_clusters

    try:
        k_options = range(2, 6)
        best_k = max(k_options, key=lambda k: silhouette_score(X_scaled, KMeans(n_clusters=k).fit_predict(X_scaled)))
    except:
        best_k = 2

    k_means = KMeans(n_clusters=best_k, max_iter=max_iter)
    k_means.fit(X_scaled)
    if mode == 0:
        try:
            silhouette_coef = silhouette_score(X_scaled, k_means.labels_)
        except ValueError:
            silhouette_coef = -1  # Assigning lowest score if clustering fails
        return silhouette_coef, k_means.labels_
    if mode == 1:
        return k_means.labels_


"""
Performs EM clustering using the data from selected_features.
If mode = 0, the silhouette score of the clustering is returned.
If mode = 1, the labels of the clustering is returned.
"""
def em_clustering(selected_features, mode, n_clusters=2):
    """
    Perform EM Clustering on selected features and return silhouette score.
        
    Returns:
    --------
    float
        Silhouette score of the clustering (-1 if clustering fails)
    """
    # Filter the selected features
    X = selected_features
    
    # Standardize selected features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Initialize and fit the EM model
    em_model = GaussianMixture(
        n_components=n_clusters,
        #random_state=0, #THOUGHTS: We can improve this later to have an array of seeds to select from to observe variations
        n_init=10  # Multiple initializations to avoid local optima
    )
    
   
    try:
        # Fit the model and get cluster assignments
        em_model.fit(X_scaled)
        labels = em_model.predict(X_scaled)
        
        # Calculate silhouette score
        silhouette_coef = silhouette_score(X_scaled, labels)
    except Exception as e:
        #print(f"Clustering failed: {str(e)}")
        silhouette_coef = -1  # Assigning lowest score if clustering fails
    if mode == 0:
        return silhouette_coef, labels
    if mode == 1:
        return labels


"""
Performs DBSCAN clustering using the data from selected_features.
If mode = 0, the silhouette score of the clustering is returned.
If mode = 1, the labels of the clustering is returned.
"""
def dbscan_clustering(selected_features, mode, eps=0.5, min_samples=5):
    """
    Perform DBSCAN clustering on selected features
    
    Parameters:
    selected_features : pandas DataFrame
        The features selected for clustering
    eps : float
        The maximum distance between two samples for them to be considered neighbors
    min_samples : int
        The number of samples in a neighborhood for a point to be considered a core point
        
    Returns:
    float : silhouette coefficient
    dict : additional clustering information
    """

    # Filter the selected features
    X = selected_features
    
    # Standardize selected features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Initialize and fit DBSCAN
    #min_samples = max(5, int(len(X) * 0.01)) # use 1% of the data as the size of the smallest sample, if this value is less than 5, default to 5
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(X_scaled)

    if -1 in labels:
        labels[labels == -1] = max(labels) + 1

    # Get number of clusters (excluding noise points which are labeled -1, K Medoids does not have noise points)
    n_clusters = len(set(labels))
    
    # calculate silhouette score if more than one cluster and  noise points
    if n_clusters > 1:
        silhouette_coef = silhouette_score(X_scaled, labels)
    else:
        silhouette_coef = -1  # Assign lowest score if clustering fails

    
    # NOTE: -- Uncomment when we analyze and optimize ---- Additional clustering information
    # info = {
    #     'n_clusters': n_clusters,
    #     'n_noise': list(labels).count(-1),
    #     'labels': labels,
    #     'cluster_sizes': pd.Series(labels).value_counts().to_dict()
    # }
    
    if mode == 0:
        return silhouette_coef, labels
    if mode == 1:
        return labels


"""
Performs KMediods clustering using the data from selected_features.
If mode = 0, the silhouette score of the clustering is returned.
If mode = 1, the labels of the clustering is returned.
"""
def kmedoids_clustering(selected_features, mode, n_clusters=2):
    # Filter the selected features
    X = selected_features
    
    # Standardize selected features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    best_k = n_clusters
    try:
        k_options = range(2, 6)
        best_k = max(k_options, key=lambda k: silhouette_score(X_scaled, KMedoids(n_clusters=k, method='alternate', nit='k-medoids++', max_iter=1500).fit_predict(X_scaled)))
    except:
        best_k = 2

     # Initialize and fit the K-Medoids model
    kmedoids = KMedoids(n_clusters=best_k, method='alternate', init='k-medoids++', max_iter=1500)
    

    # Calculate silhouette score
    try:
        labels = kmedoids.fit_predict(X_scaled)
        if len(set(labels)) > 1:
            silhouette_coef = silhouette_score(X_scaled, labels)
        else:
            silhouette_coef = -1 # Assigning lowest score if there is only 1 cluster
    except Exception as e:
        silhouette_coef = -1  # Assigning lowest score if clustering fails
    if mode == 0:
        return silhouette_coef, labels
    if mode == 1:
        return labels
    

"""
Performs Mean Shift clustering using the data from selected_features.
If mode = 0, the silhouette score of the clustering is returned.
If mode = 1, the labels of the clustering is returned.
"""
def meanshift_clustering(selected_features, mode, quantile=0.3, n_samples=500):
    # Filter the selected features
    X = selected_features
    
    # Standardize selected features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Estimate optimal bandwidth
    bandwidth = estimate_bandwidth(X_scaled, quantile=quantile, n_samples=n_samples)
    if bandwidth <= 0:
        bandwidth = 1.0  # Fallback in case of extremely small bandwidth
        
    # Initialize and fit the Mean Shift model
    meanshift = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    # Calculate silhouette score
    try:
        # print("in try")
        labels = meanshift.fit_predict(X_scaled)
        n_clusters = len(set(labels))

        # if -1 in labels:
        #     labels[labels == -1] = n_clusters - 1
        # Check the number of clusters determined 
        #n_clusters = len(np.unique(labels))
        #print(f"Number of clusters found: {n_clusters}")
        if n_clusters > 1:
            silhouette_coef = silhouette_score(X_scaled, labels)
        else:
            silhouette_coef = -1
    except Exception as e:
        # print("in except")
        silhouette_coef = -1  # Assign lowest score if clustering fails
    if mode == 0:
        return silhouette_coef, labels
    if mode == 1:
        return labels
    
##### HELPER FUNCTIONS #####
"""
Converts the binary value of state (which represents features selected) 
to both list features and string output res. If mode = 0, returns features.
If mode = 1, returns res.
"""
def bin_to_features(state, mode):
  state_bin = bin(state)
  #print(state_bin)
  state_bin_arr = np.array([b for b in state_bin[2:]])
  #pad with zeros
  diff = len(FEATURES) - len(state_bin_arr)
  padded_arr = np.insert(state_bin_arr, 0, ['0' for i in range(diff)])
  (padded_arr)

  # identify which indexes are 1
  idx = (np.where(padded_arr == '1')[0]).tolist()
  #print(idx)
  # select feature headings
  selected_features = OG_FEATURES.iloc[:,idx]
  features = selected_features.columns.tolist()
  res = f"Features Used: {features}"
  if mode == 0: # return actual feature list
    return selected_features
  if mode == 1: # return string of feature list
    return res
  

def algorithm_prep(state, action, mode):
  selected_features = bin_to_features(state, 0)
  
  # call algorithm function
  out = None
  #print('algorithm:',ALGORITHMS[action])

  # if mode = 0, output is the silhouette coefficient
  # if mode = 1, output is the cluster labelling
  match action:   
    case 0:
      #print('algorithm:',ALGORITHMS[action])
      out = dbscan_clustering(selected_features, mode)
    case 1: 
      #print('algorithm:',ALGORITHMS[action])
      out = meanshift_clustering(selected_features, mode)
    case 2:
      #print('algorithm:',ALGORITHMS[action])
      out = kmedoids_clustering(selected_features, mode)
    case 3: 
      out = em_clustering(selected_features, mode)
    case 4:
      out = kmeans_clustering(selected_features, mode)
  return out
    

##### REINFORCEMENT LEARNING #####
# Markov Decision Process (MDP) - The Bellman equations adapted to
# Q Learning.Reinforcement Learning with the Q action-value(reward) function.
# Copyright 2018 Denis Rothman MIT License. See LICENSE.
import numpy as ql

def RL(data, original_features_scaled):

    # R is The Reward Matrix for each state
    # 1024 configurations of the 10 features --> 2^10
    # 5 algorithms
    num_configs = 2 ** len(FEATURES)
    R = ql.matrix(ql.zeros([num_configs,NUM_ALG]))

    # Q is the Learning Matrix in which rewards will be learned/stored
    Q = ql.matrix(ql.zeros([num_configs,NUM_ALG]))

    # used to save the labels of each (state, action) combination for later retrieval
    cluster_labels_matrix = np.empty(Q.shape, dtype=object)

    # Gamma : It's a form of penalty or uncertainty for learning
    # If the value is 1 , the rewards would be too high.
    # This way the system knows it is learning.
    gamma = 0.8

    # The possible "a" actions when the agent is in a given state
    def possible_actions(state):
        # 2) DONE: we should check Q, not R because R is never modified
        current_state_row = Q[state,]
        # 3) DONE: this should pick valid actions based on what we have not visited
        possible_act = ql.where(current_state_row == 0)[1]
        return possible_act


    # This function chooses at random which action to be performed within the range 
    # of all the available actions.

    def ActionChoice(available_actions_range, state):
        epsilon = 0.95 # 90% exploration
        if len(available_actions_range) > 0:
            if np.random.rand() < epsilon:  
                # Explore: Randomly pick from possible actions
                next_action = int(ql.random.choice(available_actions_range, 1)[0])
            else:
                # Exploit: Pick best action from Q matrix
                next_action = int(np.argmax(Q[state, :]))
        else:
        # If no valid actions, pick randomly from all possible algorithms
            next_action = int(np.random.choice(NUM_ALG, 1)[0])
        
        return next_action
        


    # A version of Bellman's equation for reinforcement learning using the Q function
    # This reinforcement algorithm is a memoryless process
    # The transition function T from one state to another
    # is not in the equation below.  T is done by the random choice above

    def reward(current_state, action, gamma):
        Max_State = ql.where(Q[action,] == ql.max(Q[action,]))[1]

        if Max_State.shape[0] > 1:
            Max_State = int(ql.random.choice(Max_State, size = 1)[0])
        else:
            Max_State = int(Max_State[0])

        MaxValue = Q[Max_State, action]

        # call function to run ML algorithm using the value of action. this will
        # run the algorithm using the features from current_state, create clusters,
        # and calculate the silhouette value.
        selected_silhouette_co, labels = algorithm_prep(current_state, action, 0)
        cluster_labels_matrix[current_state, action] = labels
        try:
            overall_silhouette_co = silhouette_score(original_features_scaled, labels)
        except ValueError: overall_silhouette_co = -1

        # calculate ratio of selected features 
        ratio = selected_silhouette_co / (overall_silhouette_co + 1e-6)
        if selected_silhouette_co < overall_silhouette_co:
            penalty = 0.1 * ratio
        else: penalty = 0
        
        # Bellman's MDP based Q function

        # normalized silhouette score for better consistency in reinforcement learning
        if selected_silhouette_co < 0: # ensures RL doesn't learn from bad clustering
            norm_silhouette = 0
        else:
            norm_silhouette = (selected_silhouette_co + 1) / 2  # Scale from [-1,1] to [0,1]
        # norm_silhouette = (selected_silhouette_co + 1) / 2
        
        #norm_silhouette = (silhouette_co + 1) / 2  # Scale from [-1,1] to [0,1]
        # Q[current_state, action] = norm_silhouette + gamma * MaxValue
        Q[current_state, action] = (norm_silhouette - penalty) + gamma * MaxValue


    # Learning over n iterations depending on the convergence of the system
    # A convergence function can replace the systematic repeating of the process
    # by comparing the sum of the Q matrix to that of Q matrix n-1 in the
    # previous episode

    # agent_s_state. The agent the name of the system calculating
    # s is the state the agent is going from and s' the state it's going to
    # this state can be random or it can be chosen as long as the rest of the choices
    # are not determined. Randomness is part of this stochastic process
    # 1) DONE: decide if starting state is random or a specific state
    #agent_s_state = 1

    # Get available actions in the current state
    #PossibleAction = possible_actions(agent_s_state)

    # Sample next action to be performed
    #action = ActionChoice(PossibleAction, agent_s_state)

    # Rewarding Q matrix
    #reward(agent_s_state,action,gamma)


    #state_epsilon = 0.95 # 5% exploration
    visited_pairs = np.zeros(Q.shape, dtype=bool)
    for a in range(NUM_ALG):
        visited_pairs[0,a] = True # to skip all null feature configs

    convergence_threshold = 0.01  
    previous_Q = Q.copy()
    iteration_buffer = num_configs * NUM_ALG

    for i in range(10000):
        print("Iteration:", i)
        
        # visit all states first, then allow full access to any state
        unvisited_pairs = np.argwhere(visited_pairs == False)
        state_epsilon = max(0.1, 0.95 * (0.99 ** i)) # starts at 5% exploration/95% exploitation. exploration increases over time but is capped at 90%. 

        if len(unvisited_pairs) > 0 and ql.random.rand() < state_epsilon:
            current_pair = unvisited_pairs[ql.random.choice(len(unvisited_pairs))]
            current_state, action = current_pair
        else:
            if len(unvisited_pairs) == 0:
                print('all pairs visited')
            if ql.random.rand() < state_epsilon: # explore
                current_state = ql.random.randint(1, int(Q.shape[0]))
            else: # exploit past good states
                k = 10
                top_k_states = np.argsort(np.array(Q.sum(axis=1)).flatten())[-k:]
                current_state = np.random.choice(top_k_states)
            PossibleAction = possible_actions(current_state)
            action = ActionChoice(PossibleAction, current_state)
        visited_pairs[current_state, action] = True  
        
        # print("Algorithm:", ALGORITHMS[action])
        reward(current_state,action,gamma)
        #visited_states.add((current_state, action))

        if i > iteration_buffer: # make sure it doesn't stop too early
        # check for convergence in Q to stop updates
            Q_diff = np.abs(Q - previous_Q).sum()
            if Q_diff < convergence_threshold:
                print(f"Converged at iteration {i} with Q_diff={Q_diff:.4f}")
                break

        previous_Q = Q.copy() # update for comparison
        # 95% of the time, we choose the random action and state 
        
    # Displaying Q before the norm of Q phase
    # print("Q:")
    # print(Q)

    # Norm of Q
    # print("Normed Q:")
    # print(Q/ql.max(Q)*100)

    # DONE: get maximum value from Q-Learning Matrix
    normed_Q = Q/ql.max(Q)*100
    max_location = np.where(normed_Q==normed_Q.max())
    # print("\nmax value located at",max_location)
    max_config = max_location[0][0]
    max_algorithm = max_location[1][0]
    final_feats = bin_to_features(max_config, 1)
    # print(f"\nUsing algorithm {ALGORITHMS[max_algorithm]} and {final_feats}, max value is:",normed_Q[max_config,max_algorithm])
    #DONE: print(f"Selected features:")

    # get final cluster labels
    cluster_labels = cluster_labels_matrix[max_config, max_algorithm]

    # match data to their clusters
    labelled_data = data.copy()
    labelled_data['cluster'] = cluster_labels

    # get total number of clusters
    num_clusters = labelled_data['cluster'].nunique()

    ### filter clusters based on percentage of data

    # # for each unique value, get the count / len of data (aka percentage)
    # cluster_array = labelled_data['cluster'].to_numpy()
    # perc_values = np.unique(cluster_array,return_counts = True)[-1]
    # percentages = perc_values / labelled_data.shape[0]

    # # keep cluster values with % < 10 as anomalous
    # idx = (np.where(percentages <= 0.1)[0]).tolist()
    # anomalies = labelled_data.loc[labelled_data['cluster'].isin(idx)]


    ### filter anomalous clusters by size relative to the data statistics
    cluster_sizes = labelled_data['cluster'].value_counts(normalize=True)
    mean_size = cluster_sizes.mean()
    std_dev = cluster_sizes.std()
    flag_val = mean_size
    anomalous_clusters = cluster_sizes[cluster_sizes < flag_val].index
    anomalies = labelled_data[labelled_data['cluster'].isin(anomalous_clusters)]

    # if none fall below the threshold, check if smallest two are statistically different
    if len(anomalous_clusters) == 0:
        sorted_clusters = cluster_sizes.sort_values()
        sm, sec_sm = sorted_clusters.iloc[0], sorted_clusters.iloc[1]

        if sm < (0.8 * sec_sm):  # sm is at least 20% smaller than sec_sm
            anomalies = labelled_data[labelled_data['cluster'] == sorted_clusters.index[0]]
    
    cluster_sizes = labelled_data['cluster'].value_counts(normalize=True)
    final_alg = ALGORITHMS[max_algorithm]

    return anomalies, cluster_sizes, final_feats
 

##### MAIN #####
'''

'''
def run_rl(backend_data):
    features = backend_data["features"]
    print("Selected features:", features)
    # raise Exception
    global FEATURES, ALGORITHMS, NUM_ALG, OG_FEATURES
    FEATURES = {k:str(v) for k,v in zip(range(len(features)), features) }
    data = backend_data["df"]
    ALGORITHMS = {0: 'DBSCAN Clustering', 1: 'Mean Shift', 2: 'K-Mediods', 3: 'EM Clustering', 4: 'K-Means'}
    NUM_ALG = len(ALGORITHMS)
    OG_FEATURES = data[features].copy(deep = True)
    # print(OG_FEATURES.head(10))

    scaler = StandardScaler()
    original_features_scaled = scaler.fit_transform(OG_FEATURES)
    # if backend_data["uid"] == None:
    #     data['uid'] = data.index # comment out because done in feature selection
    #     backend_data["uid"] = "uid"
    event_ids = data[backend_data["uid"]]

    anomalies, cluster_sizes, final_features = RL(data, original_features_scaled)
    return anomalies, cluster_sizes, final_features


