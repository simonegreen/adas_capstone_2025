from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from backend.backendInterface import add_data, find_anomalies, get_output,backend_data
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi import Request


# Mount routers
from backend.api.intent import router as intent_router
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
# app.include_router(interpret_router)

# Original routes
@app.post("/add_data/")
async def api_add_data(request: Request, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    try:
        # Parse ALL form fields at once
        form = await request.form()   # <-- this returns a FormData mapping
    
        uid_header = form.get("uidHeader")
        ts_header = form.get("tsHeader")
        sce_ip_header = form.get("sceIPHeader")

        print("Received form fields:", form)
        print("uid:", uid_header, "ts:", ts_header, "src:", sce_ip_header, flush=True)

        cleaned_df = add_data(file)

        # Save to backend memory
        backend_data["uid"] = uid_header
        backend_data["time"] = ts_header
        backend_data["source_ip"] = sce_ip_header

        return {
            "status": "success",
            "rows": cleaned_df.shape[0],
            "columns": cleaned_df.shape[1]
        }
    except Exception as e:
        print("[/add_data] ERROR:", repr(e), flush=True)
        raise HTTPException(status_code=400, detail="Error uploading file. Please try again")

@app.get("/find_anomalies/")
async def api_find_anomalies(query: dict | None = None, uid: str | None = None, num_features: int | None = None, ts: int | None = None, src_ip: str | None = None):
    """
    Legacy GET endpoint preserved for testing.
    If your backendInterface.find_anomalies requires (query, uid, num_feat), map them here.
    """
    try:
        anomalies = find_anomalies(query, uid, num_features, ts, src_ip)
        return anomalies.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/get_output/")
async def api_get_output(query: dict | None = None):
    """
    Legacy GET endpoint preserved for testing.
    """
    try:
        output = get_output() if query is None else get_output()  # keep signature if your function ignores query
        return output # output is a dictionary
        # If get_output returns a DataFrame:
        # try:
        #     return output.to_dict(orient="records")
        # except Exception:
        #     return {"result": output}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
