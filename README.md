# Autonomous Data Scientist for Network Traffic Anomaly Detection
This project aims to integrate unsupervised clustering algorithms,
automated feature selection, and reinforcement learning into
an autonomous agent with the ability to detect anomalous behavior in network traffic.

## Data Sets
### ChatGPT Generated Data
The dataset used in Trial 1 is : [Generated Dataset - Combined Sources](data/generated/raw/combined_source_data.csv).<br/>
- It consists of artificially generated network traffic data from 9 emulated sources.
### Aposemat IoT-23 Data
The dataset used in Trial 2 is: [CTU-IoT-Malware-Capture-20-1](data/real-world/raw/CTU-IoT-Malware-Capture-21-1conn.log.labeled.csv).<br/>
- It is part of [Aposemat IoT-23 dataset](https://www.stratosphereips.org/datasets-iot23) and consists of labeled malicious and benign IoT network traffic events

## Data Classification Procedure
The project is implemented in three distinct phases; one for the essential data preparation and two classification trials. <br/>
- Each step is represented in a corresponding notebook inside [notebooks](notebooks).
- Intermediary data files are stored inside the [data](data) path.

### PHASE 1 - Initial Data Prep
> Corresponding notebook:  [data_prep.ipynb](data_prep.ipynb)

Implemented data exploration and cleaning tasks: </br>
1. Load the dataset into a Pandas DataFrame
2. Convert qualitative columns to numerical values using mapping.
3. Drop columns with more than half unique values, single unique values, or containing NaN.
4. Standardize numerical columns using StandardScaler to ensure consistent scaling.
5. Apply PCA (Principal Component Analysis) to reduce dimensionality by selecting the most influential features </br>
   (Note: This step was added for Trial 2 and manual feature selection was used in Trial 1)
6. Save the cleaned and reduced dataset to a new CSV file
   For Trial 1: [feature_selection_quantitative.csv](data/generated/processed/feature_selection_quantitative.csv)
   For Trial 2:
### PHASE 2 - Trial 1
> Corresponding notebook:  [Trial1.ipynb](Trial1.ipynb) </br>

This trial was implemented on the ChatGPT Generated Dataset, with the following steps:
1. Install and import necessary libraries
2. Load the cleaned dataset into a pandas DataFrame
3. Represent feature subsets using binary states
4. Initialize the Q-Matrix for feature configurations (states) and clustering algorithms (actions).
5. Set up the Bellman equation to update the matrix with rewards based on silhouette scores
6. Execute clustering algorithms (KMeans, EM Clustering, DBSCAN, K-Medoids, and Mean Shift)
7. Iterate 6000 times: select a state, run clustering, compute silhouette scores, and update the reward matrix
8. Identify the state and algorithm with the highest reward value
9. Apply the best state & action to cluster the data and assign cluster IDs
10. Identify clusters with <10% of data as anomalous
11. Extract and display IP addresses corresponding to the identified anomalous clusters
### PHASE 3 - Trial 2
> Corresponding notebook:  [Trial2.ipynb](Trial2.ipynb) </br>

This trial follows a similar process to Trial 1 with the following key differences:
1. The input data was the Real-World Data from Aposemat IOT-23
2. The features input were those chosen by the PCA automated feature selection in [data_prep.ipynb](data_prep.ipynb)
3. The iterations were increased to 10000
4. The output of the model produces a list of malicious events rather than IP addresses. These can be mapped back to the corresponding device in the raw dataset


### Results
