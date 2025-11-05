import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), "backend"))
from backend.backendInterface import add_data, find_anomalies, get_output

data_path = "/root/adas_capstone_2025/data/real-world/data-cleaning/cleaned_RW21.csv"
uid_col = "uid"

add_data(data_path)
anoms = find_anomalies(query="test", uid=uid_col, num_feat=10)

out_path = "/workspace/anomalies_RW21.csv"
try:
    anoms.to_csv(out_path, index=False)
    print(f"Saved anomalies to {out_path}")
except Exception:
    print(anoms)

print(get_output())
