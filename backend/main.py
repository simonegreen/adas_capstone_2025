from fastapi import FastAPI, File, UploadFile, HTTPException
from backend.backendInterface import add_data, find_anomalies, get_output
from fastapi.middleware.cors import CORSMiddleware

# Mount routers
from backend.api.intent import router as intent_router
from backend.api.interpret import router as interpret_router

app = FastAPI()

# Allow frontend to call API from a different origin/port
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# LLM routes
app.include_router(intent_router)
app.include_router(interpret_router)

# Original routes
@app.post("/add_data/")
async def api_add_data(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    try:
        cleaned_df = add_data(file)
        return {
            "status": "success",
            "rows": cleaned_df.shape[0],
            "columns": cleaned_df.shape[1]
        }
    except Exception:
        raise HTTPException(status_code=400, detail="Error uploading file. Please try again")

@app.get("/find_anomalies/")
async def api_find_anomalies(query: str | None = None, uid: str | None = None, num_features: int | None = None):
    """
    Legacy GET endpoint preserved for testing.
    If your backendInterface.find_anomalies requires (query, uid, num_feat), map them here.
    """
    try:
        anomalies = find_anomalies(query=query, uid=uid or "uid", num_feat=num_features or 10)
        return anomalies.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_output/")
async def api_get_output(query: str | None = None):
    """
    Legacy GET endpoint preserved for testing.
    """
    try:
        output = get_output() if query is None else get_output()  # keep signature if your function ignores query
        # If get_output returns a DataFrame:
        try:
            return output.to_dict(orient="records")
        except Exception:
            return {"result": output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
