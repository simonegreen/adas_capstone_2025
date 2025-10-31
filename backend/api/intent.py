# api/intent.py
from fastapi import APIRouter, HTTPException
from backend.LLM.router import resolve_intent
from backend.models import Intent, FindAnomaliesIn
from backend.backendInterface import backend_data
from backend.backendInterface import find_anomalies as bi_find_anomalies
from backend.backendInterface import get_output as bi_get_output

router = APIRouter(prefix="/api", tags=["intent"])

def _to_table(maybe_df):
    # Convert pandas DataFrame to list[dict] if needed
    try:
        return maybe_df.to_dict(orient="records")
    except Exception:
        return maybe_df

@router.post("/intent", response_model=dict)
async def intent(message: str):
    """
    1) Parse natural language with OpenAI → {action, params}
    2) Dispatch to existing backend functions
    3) Return normalized JSON to frontend
    """
    try:
        parsed: Intent = resolve_intent(message)
    except Exception:
        return {
            "ok": False,
            "error": "Unsupported query.",
            "hint": [
                "upload CSV at /add_data then ask: 'top 5 past_week'",
                "rerun with 15 features",
                "why IP 10.0.0.7 verbose"
            ]
        }

    act = parsed.action
    p = parsed.params

    # Require data for actions that operate on a dataset
    if act in ("find_anomalies", "get_output", "rerun") and backend_data.get("df") is None:
        raise HTTPException(400, "No dataset loaded. Upload CSV at /add_data first.")

    if act == "upload_data":
        return {
            "ok": True,
            "message": "Upload your CSV to /add_data (POST). You may specify uid_column/time_range in UI.",
            "params": p.model_dump()
        }

    if act == "find_anomalies":
        payload = FindAnomaliesIn(
            uid_column=p.uid_column or (backend_data.get("uid") or "uid"),
            time_range=p.time_range or "past_week",
            top_n=p.top_n or 5,
            num_features=p.num_features or 10,
        )
        df = bi_find_anomalies(query=None, uid=payload.uid_column, num_feat=payload.num_features)
        table = _to_table(df)
        return {
            "ok": True,
            "action": act,
            "result": {
                "summary": f"Top {payload.top_n} anomalies with {payload.num_features} features",
                "table": table[: payload.top_n] if isinstance(table, list) else table
            }
        }

    if act == "get_output":
        res = bi_get_output()
        return {"ok": True, "action": act, "result": res}

    if act == "rerun":
        nf = p.num_features or 10
        uid = backend_data.get("uid") or "uid"
        df = bi_find_anomalies(query=None, uid=uid, num_feat=nf)
        return {"ok": True, "action": act,
                "result": {"summary": f"Reran with num_features={nf}", "table": _to_table(df)}}

    if act == "reset":
        backend_data.update({"df": None, "uid": None, "features": None, "anomalies": None})
        return {"ok": True, "message": "State cleared."}

    return {"ok": False, "help": ["top 5 past_week", "rerun with 15 features", "why IP 10.0.0.7 verbose"]}

