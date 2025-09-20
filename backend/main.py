from fastapi import FastAPI, File, UploadFile, HTTPException
from backendInterface import add_data, find_anomalies, get_output

app = FastAPI()

@app.post("/add_data/")
async def api_add_data(file: UploadFile = File(...)):
    # should there be a size limit? idk how much the backend can actually store/process :/
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    try:
        cleaned_df = add_data(file)
        return {
            "status": "success",
            "rows": cleaned_df.shape[0],
            "columns": cleaned_df.shape[1]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error uploading file. Please try again")
    
@app.get("/find_anomalies/")
async def api_find_anomalies():
    # TODO: update to take in the query results from LLM
    try:
        anomalies = find_anomalies(query) #uid & num_feat from query
        return anomalies.to_dict(orient="records") #anomaly results as JSON placeholder
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/get_output/")
async def api_get_output():
    # TODO: update to take in type of output from LLM results
    try:
        output = get_output(query)
        return output.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))