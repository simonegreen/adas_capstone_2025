import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "backend"))
from backend.backendInterface import add_data, find_anomalies, get_output

data_path = "/root/adas_capstone_2025/data/real-world/data-cleaning/cleaned_RW21.csv"
structure = {"top_n":None, "num_features":None, "start":None, "end": None, "target_ip":None, "explanation": None, "sort_by": None, "uid_column": None}
add_data(data_path)
anoms = find_anomalies(query=structure, uid="uid", num_feat=10, time=None, source_ip="uid")

print(get_output())
