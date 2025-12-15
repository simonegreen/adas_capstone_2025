"""Script to generate sampled datasets from two input datasets.
Dataset A is the anomalous/malicious data, Dataset B is benign/normal data.
"""

import pandas as pd
# for zeek data, use 2022-02-06 - 2022-02-13 anomalous data and 2022-01-09 - 2022-01-16 benign data
pathA = "/workspaces/adas_capstone_2025/data/capstone-data/UWF-zeek22-anomalies.parquet"
pathB = "/workspaces/adas_capstone_2025/data/capstone-data/UWF-zeek22-benign1-16.parquet"
targetSize = 100
out_path = f"/workspaces/adas_capstone_2025/data/capstone-data/sampled_zeek22_{targetSize}.csv"


def create_sample(
	dataA_path,
	dataB_path,
	target_size,
	out_csv,
	fracA = 0.05,
	random_state = 42,
) -> pd.DataFrame:
	if target_size <= 0:
		raise ValueError("target_size must be > 0")
	if not (0.0 <= fracA <= 1.0):
		raise ValueError("fracA must be between 0 and 1")

	# dfA = pd.read_csv(dataA_path)
	# dfB = pd.read_csv(dataB_path)
	dfA = pd.read_parquet(dataA_path)
	dfB = pd.read_parquet(dataB_path)

	nA = int(round(target_size * fracA))
	nB = int(target_size) - nA

	if nA < 0 or nB < 0:
		raise ValueError("Computed sample sizes invalid")

	replaceA = len(dfA) < nA
	replaceB = len(dfB) < nB
	if replaceA:
		raise Exception(f"dataset A has only {len(dfA)} rows but {nA} requested; sampling with replacement")
	if replaceB:
		raise Exception(f"dataset B has only {len(dfB)} rows but {nB} requested; sampling with replacement")

	sampleA = dfA.sample(n=nA, random_state=random_state) if nA > 0 else dfA.iloc[0:0]
	sampleB = dfB.sample(n=nB, random_state=random_state) if nB > 0 else dfB.iloc[0:0]

	out = pd.concat([sampleA, sampleB], ignore_index=True)
	# shuffle final output
	out = out.sample(frac=1, random_state=random_state).reset_index(drop=True)

	# save output
	out.to_csv(out_csv, index=False)

	return out.shape


if __name__ == "__main__":
	create_sample(pathA, pathB, targetSize, out_path)

