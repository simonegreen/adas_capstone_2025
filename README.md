# Autonomous Data Scientist for Network Traffic Anomaly Detection
This project aims to 

## Data Sets
### ChatGPT Generated Data
The dataset used in Trial 1 is : [Generated Dataset - Combined Sources](data\generated\raw\combined_source_data.csv).<br/>
- It consists of artificially generated network traffic data from 9 sources.
### Aposemat IoT-23 Data
The dataset used in Trial 2 is: [CTU-IoT-Malware-Capture-20-1](data\real-world\raw\CTU-IoT-Malware-Capture-21-1conn.log.labeled.csv).<br/>
- It is part of [Aposemat IoT-23 dataset](https://www.stratosphereips.org/datasets-iot23) and is labeled with malicious and benign IoT network traffic events

## Data Classification Procedure
The project is implemented in three distinct phases; one for the essential data preparation and two classification trials. <br/>
- Each step is represented in a corresponding notebook inside [notebooks](notebooks).
- Intermediary data files are stored inside the [data](data) path.

### PHASE 1 - Initial Data Prep
> Corresponding notebook:  [data_prep.ipynb](data_prep.ipynb)

Implemented data exploration and cleaning tasks:
1. 
### PHASE 2 - Trial 1
> Corresponding notebook:  [Trial1_GeneratedData.ipynb](Trial1.ipynb)

### PHASE 3 - Trial 2
> Corresponding notebook:  [Trial2_RealWorldData.ipynb](Trial2.ipynb)



### Results
