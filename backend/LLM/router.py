# llm/router.py
import json
from json import JSONDecodeError
from typing import Any, Dict
from datetime import datetime, timedelta, timezone

from dateutil.relativedelta import relativedelta

from backend.LLM.client import client, MODEL
from backend.models import Intent

# Describe allowable actions & fields (for the prompt)
ACTION_ENUM = ["upload_data", "find_anomalies", "get_output", "rerun"]

# ----- Time helpers (numeric units) -----
HOUR = 1
DAY = 2
WEEK = 3
MONTH = 4
QUARTER = 5
YEAR = 6

def _iso_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")

def _start_of_week_utc(dt: datetime) -> datetime:
    """
    ISO-8601 week: weeks start on Monday.
    Python weekday(): Monday=0 .. Sunday=6.
    """
    days_since_monday = dt.weekday()  # 0 for Monday, 6 for Sunday
    base = dt - timedelta(days=days_since_monday)
    return base.replace(hour=0, minute=0, second=0, microsecond=0)

def _start_of_month(dt):   return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
def _start_of_quarter(dt):
    q = ((dt.month - 1)//3)*3 + 1
    return dt.replace(month=q, day=1, hour=0, minute=0, second=0, microsecond=0)
def _start_of_year(dt):    return dt.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

def _add(dt, unit: int, k: int) -> datetime:
    if unit == HOUR:    return dt + timedelta(hours=k)
    if unit == DAY:     return dt + timedelta(days=k)
    if unit == WEEK:    return dt + timedelta(days=7*k)
    if unit == MONTH:   return dt + relativedelta(months=k)
    if unit == QUARTER: return dt + relativedelta(months=3*k)
    if unit == YEAR:    return dt + relativedelta(years=k)
    raise ValueError(f"Unknown unit code {unit}")

def _resolve_time_to_slim_utc(spec: Dict[str, Any], now_utc: datetime | None = None) -> Dict[str, Any]:
    """
    Take a time spec with kind=relative|calendar|absolute and numeric units,
    return slim {start,end,tz} in UTC.
    """
    now_utc = now_utc or datetime.now(timezone.utc)
    kind = spec.get("kind")

    if kind == "absolute":
        # assume strings already; just normalize tz field
        return {
            "start": spec["start"],
            "end": spec["end"],
            "tz": "UTC",
        }

    if kind == "relative":
        unit = int(spec["unit"])
        n = int(spec["n"])
        rnd = int(spec.get("round", 0))

        if rnd == 0:
            # rolling window
            if n < 0:
                end_dt = now_utc
                start_dt = _add(end_dt, unit, n)  # n negative
            else:
                start_dt = now_utc
                end_dt = _add(start_dt, unit, n)
        else:
            # snap to current period start
            if unit == WEEK:
                start_dt = _start_of_week_utc(now_utc)
            elif unit == DAY:
                start_dt = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
            elif unit == MONTH:
                start_dt = _start_of_month(now_utc)
            elif unit == HOUR:
                start_dt = now_utc.replace(minute=0, second=0, microsecond=0)
            else:
                start_dt = now_utc
            end_dt = now_utc if n < 0 else _add(start_dt, unit, n)

        return {"start": _iso_utc(start_dt), "end": _iso_utc(end_dt), "tz": "UTC"}

    if kind == "calendar":
        unit = int(spec["unit"])
        offset = int(spec.get("offset", -1))

        if unit == WEEK:
            cur = _start_of_week_utc(now_utc)
            start_dt = cur + timedelta(days=7 * offset)
            end_dt = start_dt + timedelta(days=7)
        elif unit == DAY:
            cur = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
            start_dt = _add(cur, DAY, offset)
            end_dt = _add(start_dt, DAY, 1)
        elif unit == MONTH:
            cur = _start_of_month(now_utc)
            start_dt = _add(cur, MONTH, offset)
            end_dt = _add(start_dt, MONTH, 1)
        elif unit == QUARTER:
            cur = _start_of_quarter(now_utc)
            start_dt = _add(cur, QUARTER, offset)
            end_dt = _add(start_dt, QUARTER, 1)
        elif unit == YEAR:
            cur = _start_of_year(now_utc)
            start_dt = _add(cur, YEAR, offset)
            end_dt = _add(start_dt, YEAR, 1)
        else:
            raise ValueError(f"Unknown calendar unit code {unit}")

        return {"start": _iso_utc(start_dt), "end": _iso_utc(end_dt), "tz": "UTC"}

    # no kind or unsupported: just return as-is
    return spec

# ----- Prompt text -----
SCHEMA_AND_RULES = """
The "params" object may include: top_n, num_features, time, target_ip, source_ip, explanation, sort_by, uid_column.

- target_ip: IP address to explain (why this IP is anomalous).
- source_ip: IP address to filter on when finding anomalies.

TIME PARAM (numeric; never free-text like "past_week"):
- "kind": "relative" | "calendar" | "absolute"

For "relative":
  {"unit": 1|2|3|4, "n": signed integer (non-zero), "round": 0|1, "tz": "UTC"}
  Units: 1=hour, 2=day, 3=week, 4=month
  Semantics:
    - n < 0 → past (e.g., -1 = past 1 unit)
    - n > 0 → future
    - round = 0 → rolling window (past 7 days = now-7d → now)
    - round = 1 → snap to current period boundary ("this X so far")

For "calendar":
  {"unit": 2|3|4|5|6, "offset": integer, "tz": "UTC"}
  Units: 2=day, 3=week, 4=month, 5=quarter, 6=year
  - offset = -1 → previous full period (e.g., last week/month/quarter)
  - Weeks follow ISO-8601: weeks start on Monday.

For "absolute":
  {"start": ISO8601 string, "end": ISO8601 string, "tz":"UTC"}

ACTION MAPPING:
- "summary"/"report"/"overview" → action="get_output"
- "find anomalies"/"top N anomalies" → action="find_anomalies"

DEFAULTS:
- Always include top_n and num_features explicitly (use 10 if omitted).
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

def _postprocess_and_validate(raw: Dict[str, Any]) -> Intent:
    """
    - Ensure params exists
    - Fill numeric defaults
    - Convert time to slim {start,end,tz} in UTC
    - Validate with Pydantic Intent
    """
    if not isinstance(raw, dict):
        raise ValueError("Intent must be a JSON object")

    raw.setdefault("action", "")
    raw.setdefault("params", {})
    params = raw["params"]

    # Normalize action
    if isinstance(raw["action"], str):
        raw["action"] = raw["action"].strip().lower()

    # Explicit defaults
    if params.get("top_n") is None:
        params["top_n"] = 10
    if params.get("num_features") is None:
        params["num_features"] = 10

    # Normalize time to {start,end,tz} if kind is present
    t = params.get("time")
    if isinstance(t, dict) and "kind" in t:
        params["time"] = _resolve_time_to_slim_utc(t)

    # Pydantic validation
    return Intent.model_validate(raw)

def resolve_intent(user_text: str) -> Intent:
    """
    Parse natural language into {action, params} via OpenAI JSON mode,
    then normalize and validate.
    """
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
        data = json.loads(content)
        return _postprocess_and_validate(data)

    except TypeError:
        # Fallback if response_format is not supported
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text},
            ],
        )
        content = resp.choices[0].message.content or "{}"
        start = content.find("{")
        end = content.rfind("}")
        if start != -1 and end != -1 and end > start:
            payload = content[start : end + 1]
        else:
            payload = "{}"
        data = json.loads(payload)
        return _postprocess_and_validate(data)


