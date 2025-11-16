# api/intent.py
from fastapi import APIRouter, HTTPException
from ..llm.router import resolve_intent
from ..models import Intent, FindAnomaliesIn
from ..backendInterface import backend_data
from ..backendInterface import find_anomalies as bi_find_anomalies
from ..backendInterface import get_output as bi_get_output

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
    1) Use LLM to parse natural language into {action, params}
    2) Dispatch to backend functions
    3) Return normalized JSON to frontend
    """
    try:
        parsed: Intent = resolve_intent(message)
    except Exception:
        return {
            "ok": False,
            "error": "Unsupported query.",
            "hint": [
                "upload CSV at /add_data then ask: 'top 5 anomalies in the past week'",
                "rerun with 15 features",
                "why is IP 10.0.0.7 anomalous? verbose explanation",
            ],
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
            time=p.time,  # TimeResolved or None
            top_n=p.top_n or 10,
            num_features=p.num_features or 10,
        )

        start = payload.time.start if payload.time else None
        end   = payload.time.end   if payload.time else None

        df = bi_find_anomalies(
            query=None,
            uid=payload.uid_column,
            num_feat=payload.num_features,
            start=start,
            end=end,
            source_ip=p.source_ip,   
        )

        table = _to_table(df)

        return {
            "ok": True,
            "action": act,
            "result": {
                "summary": f"Top {payload.top_n} anomalies with {payload.num_features} features",
                "table": table[: payload.top_n] if isinstance(table, list) else table,
                "time_used": payload.time.model_dump() if payload.time else None,
                "source_ip": p.source_ip,
            },
        }

    if act == "get_output":
        # TODO: the query dict has to be in the shape backendInterface.get_output expects
        query = {
            "top_n":       p.top_n or 10,
            "num_features": p.num_features or 10,
            "start":       p.time.start if p.time else None,
            "end":         p.time.end   if p.time else None,
            "target_ip":   p.target_ip,
            "explanation": p.explanation or "verbose",
            "sort_by":     p.sort_by,
            "uid_column":  p.uid_column or (backend_data.get("uid") or "uid"),
        }

        res = bi_get_output(query)

        # TODO: check again when backend function is done
        return {
            "ok": True,
            "action": act,
            "result": res,
        }


    if act == "rerun":
        nf = p.num_features or 10
        uid = backend_data.get("uid") or "uid"
        # TODO: the query dict has to be in the shape backendInterface.get_output expects
        query = {
            "top_n":       None,
            "num_features": nf,
            "start":       None,
            "end":         None,
            "target_ip":   None,
            "explanation": None,
            "sort_by":     None,
            "uid_column":  uid,
        }

        df = bi_find_anomalies(
            query=query,
            uid=uid,
            num_feat=nf,
            time=None,
            source_ip=None,
        )

        return {
            "ok": True,
            "action": act,
            "result": {
                "summary": f"Reran with num_features={nf}",
                "table": _to_table(df),
            },
        }





