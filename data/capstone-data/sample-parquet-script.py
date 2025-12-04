import os, sys
import pandas as pd

file_path = "/workspaces/adas_capstone_2025/data/capstone-data/zeek-pq-00.parquet"
df = pd.read_parquet(file_path)

print(df.shape) 

sample = df.sample(n=3000)
print(sample.shape)

sample.to_csv("/workspaces/adas_capstone_2025/data/sample.csv", index=False)
