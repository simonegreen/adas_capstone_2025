# api/interpret.py
import json
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from backend.LLM.client import client, MODEL
from backend.models import InterpretIn, InterpretOut
from backend.backendInterface import backend_data

# router = APIRouter(tags=["interpret"])
router = APIRouter(prefix="/api", tags=["interpret"])

@router.post("/interpret", response_model=InterpretOut)
async def api_interpret(body: InterpretIn) -> InterpretOut:
    """
    Use Chat Completions + tool calling to extract numeric fields only:
    top_n and num_features. Do not include uid_column or time_range.
    """
    if backend_data.get("df") is None:
        raise HTTPException(400, "No dataset uploaded yet. Please upload a CSV first.")

    tool_schema = {
        "type": "function",
        "function": {
            "name": "find_anomalies",
            "description": "Extract numeric arguments only (top_n, num_features).",
            "parameters": {
                "type": "object",
                "properties": {
                    "top_n":        {"type": "integer", "minimum": 1, "maximum": 100, "default": 10},
                    "num_features": {"type": "integer", "minimum": 1, "maximum": 1024, "default": 10}
                },
                "additionalProperties": False
            }
        }
    }

    sys = (
        "You are a tool-calling assistant. "
        "Given a user query about anomalies, call the function exactly once "
        "with only top_n and num_features. "
        "Do NOT include uid_column or time_range; the UI supplies those."
    )

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": sys},
                  {"role": "user", "content": body.text}],
        tools=[tool_schema],
        tool_choice="auto",
    )

    call = resp.choices[0].message.tool_calls[0] if resp.choices[0].message.tool_calls else None
    if not call:
        return InterpretOut()  # fallback: 10/10

    try:
        args = json.loads(call.function.arguments or "{}")
        return InterpretOut(**args)
    except (ValidationError, Exception):
        return InterpretOut()

