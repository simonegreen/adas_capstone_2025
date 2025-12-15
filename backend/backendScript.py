
# Take on the role of the API. You should only be calling from main and/or backendInterface. 
# specify data file path
import os, sys
# sys.path.insert(0, os.path.join(os.getcwd(), "backend"))
from backend.backendInterface import add_data, find_anomalies, get_output
import asyncio

# data_path = "/workspaces/adas_capstone_2025/data/real-world/data-cleaning/cleaned_RW21.csv"
# data_path = "/workspaces/adas_capstone_2025/data/capstone-data/100-entry-test-zeek-data.csv"
data_path = "data/capstone-data/sampled_zeek22_500.csv"
query = {"top_n":3, "num_features":10, "start":None, "end": None, "target_ip":None, "explanation": "verbose", "sort_by": None, "uid_column": "uid"}
print("add data")
add_data(data_path)
print("find anomalies")
anoms = find_anomalies(query=query, uid="uid", num_feat=10, time="datetime", source_ip="src_ip_zeek")
print("get output")
out =  asyncio.run(get_output(query))

# try:
#     anoms.to_csv(out_path, index=False)
#     print(f"Saved anomalies to {out_path}")
# except Exception:
#     print(anoms)

print(out)

# TO-DO:
# - update max iterations to 1.5/2 x number of configurations
# - look at ways to improve PCA