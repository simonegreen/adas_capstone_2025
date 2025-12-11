# This contains the functions that the front end interface will have access to.
# Only this module will be imported to main for API calls.

# Imports
import pandas as pd
import numpy as np
import requests, json, ipaddress
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from datetime import datetime, timedelta
from dateutil.parser import parse
from fastapi import HTTPException
from backend.reinforcementLearning import run_rl
# from backend.featureMapping import explain_features



backend_data = {"df": pd.DataFrame,
                "uid": None,
                "time": None,
                "epoch_time": None,
                "source_ip": None,
                "int_source_ip": None,
                "features": None,
                "final_features": None,
                "anomalies": None
                } #the backend "memory"

##### DATA PREPARATION #####
def ip_to_int(ip):
    if ":" not in ip:   # IPv4
        a, b, c, d = ip.split('.')
        return (int(a)<<24) + (int(b)<<16) + (int(c)<<8) + int(d)
    else:               # IPv6
        return int(ipaddress.IPv6Address(ip))

'''
Summary: Takes in user-uploaded data, cleans it, and sets the global dataframe.
Input: file (CSV file)
Output: cleaned_df (Pandas DataFrame)
'''
def add_data(file):
    # print(type(file))
    # if not hasattr(file, "filename") or not file.filename.lower().endswith(".csv"):
    #     raise ValueError("Only CSV files are allowed")
    
    raw_file = pd.read_csv(file.file if hasattr(file, "file") else file)
    cleaned_df = clean_data(raw_file)
    backend_data["df"] = cleaned_df
    # print("At add data", cleaned_df.columns)
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
    # print("Current columns", df.columns)
    # print(f"Original shape: {original_shape}, New shape: {df.shape}")
    
    return df

###### FEATURE SELECTION & FIND ANOMALIES #####

'''
Summary: Takes the user query, performs feature selection and RL. Updates all global data.
Input: 
Output:
'''
def find_anomalies(query, uid, num_feat, time, source_ip):
    ## VAR SETUP
    df = backend_data["df"]
    # print("in find anomalies:", df.columns)
    # print("Data shape:", df.shape)    
    # print("num_feat:", num_feat)
    # print("uid:", uid)
    # print("time:", time)
    # print("source_ip:", source_ip)
    
    # raise HTTPException(status_code=501, detail="Function not yet implemented.")


    if uid is None: 
        uid = "uid"
        df[uid] = df.index
    backend_data["uid"] = uid
    # TODO: if no time filtering is specified, time can remain None. only if the query contains time filtering, should we check
    backend_data["time"] = time
    if time is None and query["start"] is not None:
        raise HTTPException(status_code=400, detail="No time column specified.")
    backend_data["source_ip"] = source_ip
    # print("after adding headings:", df.columns)
    # print("Using uid:", uid)
    # print("Using time:", time)
    # print("Using source_ip:", source_ip)
    # raise HTTPException(status_code=501, detail="Function not yet implemented.")
    
    # if source_ip is None and query["target_ip"] is not None:
    #     raise HTTPException(status_code=400, detail="No IP column specified.")
    main_identifiers = [uid, time, source_ip] # TODO: decide what to do with timestamp. if we don't want it to be a feature, add here
    
    ## FEATURE SELECTION
    num_entries = df.shape[0]
    drop = []
    for i in df:
        if df[i].dtype == 'O' and i not in main_identifiers: # qualitative
            qual_to_quant(df, i)
            if df[i].nunique() > (num_entries / 2) or df[i].nunique() == 1: # if more than 1/2 of data points have a unique label OR all have same label, drop the column. can change this!
                drop.append(i)
    # print(drop)
    # print("before drop:", df.columns)
    cleaned_df = df.drop(columns = drop)
    #qual_to_quant(cleaned_df, uid)
    backend_data["df"] = cleaned_df
    # print("after drop:", cleaned_df.columns)

    # print(cleaned_df.columns)
    # print(cleaned_df[time])
    # print(cleaned_df[source_ip])

    # print("source_ip data type", cleaned_df[source_ip].dtype)
    # print("time data type", cleaned_df[time].dtype)
    # raise Exception("before get features")
    # print("Final Columns:", str(cleaned_df.shape[1]))
    # print(cleaned_df.head())

    pca, features = get_features(cleaned_df, num_feat, main_identifiers)

    # If scaled time or source IP selected, update name in feature list
    # if "epoch_time" in features:
    #     i = np.where(features =="epoch_time")
    #     features[i]= backend_data['time']
    # if "int_source_ip" in features:
    #     i = np.where(features == "int_source_ip")
    #     features[i]= backend_data['source_ip']
    backend_data["features"] = features
    # print(features)
    # print("got features")

    #raise Exception("got features. paused.")
    ## REINFORCEMENT LEARNING
    anomalies, cluster_sizes, final_features = run_rl(backend_data) #TODO: others for output data
    backend_data["anomalies"] = anomalies
    backend_data["final_features"] = final_features
    # print("Final Features", final_features)
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
#   print(copy.columns)
  feat_options = copy.drop(columns=main_identifiers).copy(deep=True)  # Drop columns like unique IDs that shouldn't be scaled
#   print(feat_options.columns)
  feat_options["epoch_time"] = pd.to_datetime(copy[backend_data['time']])
  
#   print(feat_options[backend_data['time']].dtype)

  
  feat_options["epoch_time"] = feat_options["epoch_time"].astype(int) // 10**9
  feat_options["int_source_ip"] = copy[backend_data['source_ip']].apply(
      lambda ip: int(ip.replace('.', ''), 16) if '.' in ip else int(ip.replace(':', ''), 16)
  )


#   feat_options["int_source_ip"] = copy[backend_data['source_ip']].str.replace('.', '')
#   feat_options["int_source_ip"] = feat_options["int_source_ip"].replace(':', '')
#   ipv4_mask = copy[backend_data['source_ip']].str.contains(r'^\d+\.\d+\.\d+\.\d+$')
#   feat_options.loc[ipv4_mask, "int_source_ip"] = ipv4_to_int_fast(copy.loc[ipv4_mask, backend_data['source_ip']])
#   feat_options.loc[~ipv4_mask, "int_source_ip"] = (copy.loc[ipv4_mask, backend_data['source_ip']].apply(lambda x: int(ipaddress.ip_address(x)))
# )

#   feat_options["int_source_ip"] = copy[backend_data['source_ip']].apply(hash_ip)
  
#   print("time!")
#   print(feat_options["epoch_time"].dtype)
#   print(feat_options["epoch_time"])

#   print("ip!")
#   print(feat_options["int_source_ip"].dtype)
#   print(feat_options["int_source_ip"])

  feat_options = feat_options.replace([np.inf, -np.inf], np.nan)
  feat_options = feat_options.fillna(0)  # or use median filling

  for col in feat_options.columns:
    col_data = feat_options[col]

    if col_data.isna().any():
        print(f"❗ NaNs in {col}")

    if np.isinf(col_data).any():
        print(f"❗ Inf detected in: {col}")

    if (col_data.abs() > np.finfo(np.float64).max).any():
        print(f"❗ Overflow! Too large for float64 in: {col}")

    # print("Max per column:")
    # print(feat_options.max())
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
  #print("Most Important Features:", most_important_names.tolist())

  # Return the unique top features
  unique_feats = np.unique(most_important_names)
  #print("Unique Features:", unique_feats.tolist())

  # Return the selected unique features
  backend_data["df"]["int_source_ip"] = feat_options["int_source_ip"]
  backend_data["df"]["epoch_time"] = feat_options["epoch_time"]

  return pca, unique_feats


##### GET OUTPUT #####

'''
Summary
Input:
Output:
'''
def get_output(query):
    format = {"top_n": query["top_n"], "time_range": (query['start'], query['end']), "target_ip": query["target_ip"], "explain": query["explanation"], "sortby": query["sort_by"]} #starts with defaults
    csv = backend_data['anomalies'].to_csv(compression={'method': 'gzip'})
    output_data = backend_data["anomalies"].copy(deep=True)
    # top_n: select the top n IP addresses ONLY, do at end of all other formatting
        # maybe default to -1 or None?
    # time_range: filter based on start and end date. these will probably be integers
    # target_ip: look for this IP ONLY. start with this formatting, and return error if IP is not found
        # default to None
    # explain: ["none", "simple", "verbose"]
    # ON HOLD: sort: ["ip", "time", "quantity", "score"]

    if backend_data["time"] is None and query["start"] is not None:
        raise HTTPException(status_code=400, detail="No time column specified.")
    
    # target ip - drop all but where IP is found
    #print(f"Outputing target IP {format["target_ip"]}")
    if query["target_ip"] is not None:
        targeted_df = output_data[output_data[backend_data['source_ip']] == format["target_ip"]]
        # check if df is empty; return error if so
        if targeted_df.empty:
            raise HTTPException(status_code=400, detail="Target IP not found.")
    else: targeted_df = output_data

    # time range - drop all that have ts not within timerange
    print(f"Outputing within specified time range {format["time_range"]}")
    # drop where time < start and time > end
    
    start, end = format['time_range']
    if start is None: start = "0001-01-01 00:00:00"
    if end is None: end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Outputing within time range {start, end}")


    # convert start, end, and time column to DT naive
    start = parse(start).replace(tzinfo=None)
    end = parse(end).replace(tzinfo=None)
    targeted_df['datetime-parsed'] = targeted_df[backend_data['time']].apply(lambda x: parse(x).replace(tzinfo=None))
    timefilter_df = targeted_df[
        (targeted_df['datetime-parsed'] >= start) &
        (targeted_df['datetime-parsed'] <= end)
    ]
    
    # top n - find top n IPs by quantity. only keep those
    IP_count = timefilter_df[backend_data['source_ip']].value_counts()
    top_n_values = IP_count.head(format["top_n"])
    top_vals = top_n_values.index.tolist()
    topn_df = timefilter_df[timefilter_df[backend_data['source_ip']].isin(top_vals)]
    #print(f"Outputing top {format["top_n"]} IPs")
    
    # explanation
    # res = asyncio.run(explain_features(backend_data["final_features"]))
    # print("final_features:", backend_data["final_features"])
    # res = await explain_features(backend_data["final_features"])
    # feat_dict = res.final_output.model_dump()
    # final_feature_expl = feat_dict['features']
    lookups = None
    ip_addresses = topn_df[backend_data["source_ip"]].unique().tolist()
    try:
        # print("IP addresses for VT lookup:", ip_addresses)
        vt_reports = VT_results(ip_addresses)
    except:
        vt_reports = [{i:"None Found"} for i in ip_addresses]
    match format["explain"]:
        case None:
            #print(format["explain"])
            explain = "See anomalies below."
        case "none":
            #print(format["explain"])
            explain = "See anomalies below."
        case "simple":
            #print(format["explain"])
            explain = "See downloaded file 'final_features_expl.json' for features used to detect anomalies."
            print("Generating feature explanation JSON...")
            print("final_features:", backend_data["final_features"])
            lookups = vt_reports
            # explain = final_feature_expl
        case "verbose":
            #print(format["explain"])
            # explain = f"The following features were used to detect anomalies:\n{backend_data["final_features"]} \n See VirusTotal IP reporting below:"
            # explain = final_feature_expl
            explain = "See downloaded file 'final_features_expl.json' for features used to detect anomalies."
            print("Generating feature explanation JSON...")
            print("final_features:", backend_data["final_features"])
            lookups = vt_reports

    # ON HOLD: sort - choose what column to sort by, default is by IP in desc quantity
    #return output_data
    output_data = topn_df.sort_values(by=backend_data['source_ip'])
    keep_columns = [backend_data["source_ip"], backend_data["uid"], backend_data["time"]] + backend_data["final_features"]
    filtered_output_data = output_data[keep_columns]
    print("anomaly shape:", filtered_output_data.shape)
    output_dict = {
    'cols': filtered_output_data.columns.tolist(),
    'rows': filtered_output_data.values.tolist()
    }
    # structure anomaly output data
    return {'explain':explain, 'vt_lookups': lookups, 'anomalies': output_dict, 'csv': csv}

# def hash_ip(ip: str) -> int:
#     h = hashlib.blake2b(ip.encode(), digest_size=8)  # 8 bytes = 64-bit
#     return int.from_bytes(h.digest(), byteorder='big', signed=False)

def store_explain_features(feature_explanations):
    backend_data["feature_explanations"] = feature_explanations

def VT_results(ips):
    reports = {}
    for i in ips:

        url = f"https://www.virustotal.com/api/v3/ip_addresses/{i}"
        headers = {
            "accept": "application/json",
            "x-apikey": "01410d4672179ea9b771121c8b8782d5e24190710598a532755234bf24fcf026"
            }

        response = requests.get(url, headers=headers)
        #print(type(response))
        response_json = json.loads(response.text)
        #print(type(response_json))

        parsed_response = {"country": response_json["data"]["attributes"]["country"], "reputation": response_json["data"]["attributes"]["reputation"], "stats": response_json["data"]["attributes"]["last_analysis_stats"]}
        #print(parsed_response)
        reports[i] = parsed_response
    #print(reports)
    return reports


# sample query
# structure = {"top_n":None, "num_features":None, "start":None, "end": None, "target_ip":None, "explanation": None, "sort_by": None, "uid_column": None}

# IP_error = {"top_n":None, "num_features":None, "start":None, "end": None, "target_ip":"1.2.3.4", "explanation": None, "sort_by": None, "uid_column": None}
# time_error = {"top_n":None, "num_features":None, "start":1234, "end": None, "target_ip":None, "explanation": None, "sort_by": None, "uid_column": None}
# structure = {"top_n":None, "num_features":None, "start":None, "end": None, "target_ip":None, "explanation": "verbose", "sort_by": None, "uid_column": None}