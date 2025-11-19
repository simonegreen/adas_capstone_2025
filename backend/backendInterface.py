# This contains the functions that the front end interface will have access to.
# Only this module will be imported to main for API calls.

# Imports
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from backend.reinforcementLearning import run_rl


backend_data = {"df": None,
                "uid": None,
                "features": None,
                "anomalies": None
                } #the backend "memory"

##### DATA PREPARATION #####

'''
Summary: Takes in user-uploaded data, cleans it, and sets the global dataframe.
Input:
Output:
'''
def add_data(file):
    if not hasattr(file, "filename") or not file.filename.lower().endswith(".csv"):
        raise ValueError("Only CSV files are allowed")
    
    raw_file = pd.read_csv(file.file if hasattr(file, "file") else file)
    cleaned_df = clean_data(raw_file)
    backend_data["df"] = cleaned_df
    return cleaned_df

def clean_data(df):
    # print("# Starting Columns:", str(df.shape[1]))
    original_columns = df.columns.tolist()
    original_shape = (df.shape[0], df.shape[1])

    # replace blanks with NaN
    df.replace("", np.nan, inplace=True)

    # Drop columns where ALL values are NaN
    df.dropna(axis=1, how='all', inplace=True)

    # Drop rows where ANY value is NaN
    df.dropna(axis=0, how='any', inplace=True)

    # Identify which rows/columns were dropped
    dropped_columns = list(set(original_columns) - set(df.columns))
    # print("Dropped columns:", dropped_columns)
    # print(f"Original shape: {original_shape}, New shape: {df.shape}")
    
    return df

###### FEATURE SELECTION & FIND ANOMALIES #####

# #############TESTING PURPOSES ONLY START #############

# def find_anomalies(query, uid, num_feat, start=None, end=None, source_ip=None):
#     """
#     Lightweight test implementation for verification.
#     Produces a predictable list of dicts and stores it in backend_data['anomalies'].
#     This avoids running the heavy RL pipeline during testing.
#     """

#     # Keep the uid in backend memory
#     backend_data["uid"] = uid

#     # Determine how many mock rows to produce (use num_feat as guidance)
#     n = min(10, max(1, int(num_feat or 5)))

#     mock_table = []
#     for i in range(n):
#         mock_table.append({
#             "uid": f"{uid or 'uid'}-{i+1}",
#             "score": round(1.0 - i * 0.05, 3),
#             "rank": i + 1,
#             "num_features": num_feat,
#             "start": str(start) if start else None,
#             "end": str(end) if end else None,
#             "source_ip": source_ip,
#             "note": "mocked result for testing"
#         })

#     # Save into backend memory so get_output() can return the same results
#     backend_data["anomalies"] = mock_table

#     return mock_table

# #############TESTING PURPOSES ONLY END #############
'''
Summary: Takes the user query, performs feature selection and RL. Updates all global data.
Input:
Output:
'''
def find_anomalies(query, uid, num_feat, start=None, end=None, source_ip=None):

    ## FEATURE SELECTION
    main_identifiers = [uid] # TODO: could later add option for additional headings to ignore, otherwise switch to just UID
    backend_data["uid"] = uid
    df = backend_data["df"]
    num_entries = df.shape[0]
    drop = []
    for i in df:
        if df[i].dtype == 'O' and i not in main_identifiers: # qualitative
            qual_to_quant(df, i)
            if df[i].nunique() > (num_entries / 2) or df[i].nunique() == 1: # if more than 1/2 of data points have a unique label OR all have same label, drop the column. can change this!
                drop.append(i)
    # print(drop)
    cleaned_df = df.drop(columns = drop)
    qual_to_quant(cleaned_df, main_identifiers[0])
    backend_data["df"] = cleaned_df
    # print("Final Columns:", str(cleaned_df.shape[1]))
    # print(cleaned_df.head())

    pca, features = get_features(cleaned_df, num_feat, main_identifiers)
    backend_data["features"] = features

    ## REINFORCEMENT LEARNING
    anomalies, cluster_sizes, final_features = run_rl(backend_data) #TODO: others for output data
    backend_data["anomalies"] = anomalies
    return anomalies

'''Converts the qualitative column col in df to quantitative values'''
def qual_to_quant(df, col):
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])

"Returns an array with the indexes of the top n values in arr"
def get_top_n_idx(n, arr):
  arr = np.abs(arr)
  top = np.argpartition(arr, -n)[-n:]
  return top

'''
Returns a numpy array of the selected features from data using PCA.

PCA: develops unspecified number of components to represent data
Feature Selection: getting the top_n features that have the highest weighted
importance across all components 
'''
def get_features(data, top_n, main_identifiers):
  copy = data.copy(deep=True)  # Make a copy of the original data to avoid modifying it
  feat_options = copy.drop(columns=main_identifiers).copy(deep=True)  # Drop columns like unique IDs that shouldn't be scaled

  # Standardize the data
  scaler = StandardScaler()
  scaler.fit(feat_options)
  scaled_data = scaler.transform(feat_options)

  pca = PCA(n_components=0.95) # should represent at least 95% of overall trends in data
  pca.fit(scaled_data)

  ### USE ABSOLUTE VALUE OF LOADINGS ONLY FOR FEATURE IMPORTANCE 
  loadings = np.abs(pca.components_)  # Get importance for each feature in each component
  # feature_importance = np.sum(loadings, axis=0)  # Sum the absolute loadings for each feature across all components

  ### USE WEIGHTED LOADINGS BY EXPLAINED VARIANCE FOR FEATURE IMPORTANCE
  weighted_loadings = np.abs(pca.components_) * pca.explained_variance_ratio_.reshape(-1, 1)
  feature_importance = np.sum(weighted_loadings, axis=0)


  # Get the indexes of the top n most important features based on summed importance
  top = get_top_n_idx(top_n, feature_importance)

  # Get the feature names for the most important features
  most_important_names = feat_options.columns[top]

  # Print the selected important features
  print("Most Important Features:", most_important_names.tolist())

  # Return the unique top features
  unique_feats = np.unique(most_important_names)
  print("Unique Features:", unique_feats.tolist())

  # Return the selected unique features
  return pca, unique_feats


##### GET OUTPUT #####

'''
Summary
Input:
Output:
'''
def get_output():
    ######## JUST FOR TESTING PURPOSES ########
    return {
        "ok": True,
        "message": "Returning test results",
        "result": {
            "summary": "Returning test results"
        }
    }