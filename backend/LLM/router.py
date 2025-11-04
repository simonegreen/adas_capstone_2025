# llm/router.py
import json
from json import JSONDecodeError
from typing import Any, Dict

from .client import client, MODEL
from ..models import Intent

# Describe allowable actions & fields (for the prompt)
ACTION_ENUM = ["upload_data", "find_anomalies", "get_output", "rerun", "reset"]

SCHEMA_AND_RULES = """
The "params" object may include: top_n, num_features, time, target_ip, explanation, sort_by, uid_column.

TIME PARAM (numeric; never free-text like "past_week"):
- "kind": "relative" | "calendar" | "absolute"

For "relative":
  {"unit": 1|2|3|4, "n": signed integer (non-zero), "round": 0|1, "tz": "America/New_York"}
  Where unit codes are: 1=hour, 2=day, 3=week, 4=month
  Semantics:
    - n < 0 → past (e.g., -1 = past 1 unit)
    - n > 0 → future
    - round = 0 → rolling window (e.g., past 7 days = now-7d → now)
    - round = 1 → snap to current period boundary (“this X so far”)

For "calendar":
  {"unit": 2|3|4|5|6, "offset": integer, "tz": "America/New_York", "week_start": 0|1 (required if unit=3)}
  Where unit codes are: 2=day, 3=week, 4=month, 5=quarter, 6=year
  - offset = -1 → previous full period (e.g., last week/month)
  - week_start: 0=sunday, 1=monday

For "absolute":
  {"start": ISO8601 string, "end": ISO8601 string, "tz":"America/New_York"}

ACTION MAPPING:
- "summary"/"report"/"overview" → action="get_output"
- "find anomalies"/"top N anomalies" → action="find_anomalies"

DEFAULTS:
- If top_n is missing, set top_n=10 (include it explicitly).
- If num_features is missing, set num_features=10 (include it explicitly).
- If the user asks for a summary/report, prefer explanation="verbose".
- For "past X": use RELATIVE with signed n and round=0.
- For "last/previous X": use CALENDAR with offset=-1. If week, include week_start.
"""

SYSTEM_PROMPT = (
    "You are an intent parser for ADaS. Always return a single JSON object with keys "
    '"action" and "params". The "action" must be one of: ' + str(ACTION_ENUM) + ".\n"
    + SCHEMA_AND_RULES +
    "\nFormatting rules:\n"
    "- Output only valid JSON (no comments, no code fences, no extra text).\n"
    "- Prefer 'relative' for 'past X'; 'calendar' for 'last X'; 'absolute' for explicit dates.\n"
    "- If uncertain about a field, omit it from params rather than guessing.\n"
)

def _validate_to_intent(raw: Dict[str, Any]) -> Intent:
    # Normalize action
    if isinstance(raw, dict) and "action" in raw and isinstance(raw["action"], str):
        raw["action"] = raw["action"].strip().lower()
    # Ensure params exists
    if isinstance(raw, dict) and "params" not in raw:
        raw["params"] = {}
    # Validate
    return Intent.model_validate(raw)

def resolve_intent(user_text: str) -> Intent:
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content or "{}"
        try:
            data = json.loads(content)
        except JSONDecodeError:
            start, end = content.find("{"), content.rfind("}")
            payload = content[start:end+1] if start != -1 and end != -1 and end > start else "{}"
            data = json.loads(payload)
        # print("RAW ROUTER JSON:", json.dumps(data, indent=2))  # debug
        return _validate_to_intent(data)

    except TypeError:
        # Fallback: plain text then salvage JSON
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ]
        )
        content = resp.choices[0].message.content or "{}"
        start, end = content.find("{"), content.rfind("}")
        payload = content[start:end+1] if start != -1 and end != -1 and end > start else "{}"
        data = json.loads(payload)
        # print("RAW ROUTER JSON:", json.dumps(data, indent=2))  # debug
        return _validate_to_intent(data)


