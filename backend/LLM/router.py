# llm/router.py
import json
from typing import Any, Dict

from backend.LLM.client import client, MODEL
from backend.models import Intent

# Describe allowable actions & fields (for the prompt)
ACTION_ENUM = ["upload_data", "find_anomalies", "get_output", "rerun", "reset", "help"]

SYSTEM_PROMPT = f"""
You are an intent parser for the ADaS app. Always return a single JSON object
with keys "action" and "params". The "action" must be one of: {ACTION_ENUM}.
The "params" is an object of optional keys such as:
  - top_n: integer
  - num_features: integer
  - time_range: string like "past_day" | "past_week" | "past_month"
  - target_ip: string ip address
  - explanation: "none" | "simple" | "verbose"
  - sort_by: "ip" | "time" | "quantity" | "score"
  - uid_column: string
Never include commentary, code fences, or extra text—only valid JSON.
Infer only what is stated or strongly implied by the user text.
If uncertain about a field, omit it from "params" rather than guessing.
"""

def _validate_to_intent(raw: Dict[str, Any]) -> Intent:
    """
    Convert a raw dict (from model) into our Pydantic Intent model.
    This enforces allowed enum values and types.
    """
    # Minimal normalization (optional): lowercase action if present
    if isinstance(raw, dict) and "action" in raw and isinstance(raw["action"], str):
        raw["action"] = raw["action"].strip().lower()

    # Pydantic validation (raises if invalid)
    return Intent.model_validate(raw)


def resolve_intent(user_text: str) -> Intent:
    """
    Parse natural language into a structured {action, params} using Chat Completions JSON mode.
    Falls back to plain text -> JSON parse if JSON mode isn't available in the SDK.
    """
    # Preferred path: JSON mode (chat.completions with response_format={"type":"json_object"})
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            response_format={"type": "json_object"},  # strict JSON response
        )
        content = resp.choices[0].message.content or "{}"
        data = json.loads(content)
        return _validate_to_intent(data)

    except TypeError:
        # Some environments may not support response_format; fallback to plain text then json.loads
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ]
        )
        content = resp.choices[0].message.content or "{}"

        # Try to locate JSON in the reply (in case the model added extra text)
        # Simple heuristic: find the first '{' and last '}'.
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            payload = content[start : end + 1]
        else:
            payload = "{}"

        data = json.loads(payload)
        return _validate_to_intent(data)


