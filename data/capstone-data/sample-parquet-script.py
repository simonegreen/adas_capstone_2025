import os, sys
import pandas as pd
from sklearn.model_selection import train_test_split

file_name = "CICIDS-tuesday-capture"

# FOR PARQUET 
# file_path = f"/workspaces/adas_capstone_2025/data/capstone-data/{file_name}.parquet"
# df = pd.read_parquet(file_path)

# FOR CSV
file_path = f"/workspaces/adas_capstone_2025/data/capstone-data/{file_name}.csv"
df = pd.read_csv(file_path)

print(df.shape) 

# sample = df.sample(n=3000)

# total rows you want
sample_size = 3000
anom_label = " Label"
print(df[anom_label].value_counts())

sample, _ = train_test_split(
    df,
    train_size=sample_size,
    stratify=df[anom_label], #replace with anomaly-marked label column
    random_state=42
)


print(sample.shape)
print(sample[anom_label].value_counts())

# Uncomment to Write File
sample.to_csv(f"/workspaces/adas_capstone_2025/data/capstone-data/{file_name}-{sample_size}.csv", index=False)
