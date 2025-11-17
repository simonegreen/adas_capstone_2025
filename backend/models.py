<<<<<<< HEAD
# models.py
from pydantic import BaseModel, conint, validator
from typing import Union, Literal, Optional
from datetime import datetime

# ---- Time range ----
class TimeRangeExplicit(BaseModel):
    start: datetime
    end: datetime
    @validator("end")
    def end_after_start(cls, v, values):
        if "start" in values and v <= values["start"]:
            raise ValueError("end must be after start")
        return v

# Use underscores for presets to avoid whitespace mismatch
# TODO: change the time Literals to mmddyyyy fomat
# TODO: (later) add time range A, B (B is deafult to today) 

TimePreset = Literal["past_day", "past_week", "past_month"]
TimeRange = Union[TimePreset, TimeRangeExplicit]

# ---- Teammate's interpret models ----
class InterpretIn(BaseModel):
    text: str  # Example: "get top 3 anomalies this week"

class InterpretOut(BaseModel):
    top_n: conint(ge=1, le=100) = 10
    num_features: conint(ge=1, le=1024) = 10

class FindAnomaliesIn(BaseModel):
    uid_column: str
    time_range: TimeRange = "past_week"
    top_n: conint(ge=1, le=100) = 10
    num_features: conint(ge=1, le=1024) = 10

# NOTE: sort by score is suspended for now
# ---- Our intent models (action + params) ----
Explanation = Literal["none", "simple", "verbose"]
SortBy = Literal["ip", "time", "quantity", "score"]
Action = Literal["upload_data", "find_anomalies", "get_output", "rerun", "reset", "help"]

# TODO: update num_features default to 10, top_n default to 10, and time_range default to today
class IntentParams(BaseModel):
    top_n: Optional[conint(ge=1, le=100)] = None
    num_features: Optional[conint(ge=1, le=1024)] = None
    time_range: Optional[TimeRange] = None
    target_ip: Optional[str] = None
=======
# models.py (time spec section)
from enum import IntEnum
from pydantic import BaseModel, conint, field_validator, ValidationInfo, ConfigDict
from typing import Optional, Union, Literal
from datetime import datetime

class URel(IntEnum):
    HOUR = 1; DAY = 2; WEEK = 3; MONTH = 4

class UCal(IntEnum):
    DAY = 2; WEEK = 3; MONTH = 4; QUARTER = 5; YEAR = 6

# ----- structured time specs (for LLM output) -----
class TimeRelative(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    kind: Literal["relative"] = "relative"
    unit: URel                    # 1=hour,2=day,3=week,4=month                   
    n: int                        # signed periods; -1=past 1, +2=next 2
    round: conint(ge=0, le=1) = 0 # 0=rolling, 1=snap boundary
    tz: str = "UTC"
    @field_validator("n")
    @classmethod
    def non_zero(cls, v):
        if v == 0: raise ValueError("n cannot be 0")
        return v

class TimeCalendar(BaseModel):
    """
    Calendar-based windows (ISO-8601 style).
    Weeks always start on Monday.
    """
    model_config = ConfigDict(use_enum_values=True)
    kind: Literal["calendar"] = "calendar"
    unit: UCal                    # 2=day, 3=week, 4=month, 5=quarter, 6=year
    offset: int = -1              # -1=previous period, 0=this, +1=next
    tz: str = "UTC"


class TimeAbsolute(BaseModel):
    kind: Literal["absolute"] = "absolute"
    start: datetime
    end: datetime
    tz: Optional[str] = "UTC"

    @field_validator("end")
    @classmethod
    def end_after_start(cls, v: datetime, info: ValidationInfo) -> datetime:
        """
        Ensure end > start for absolute time windows.
        In Pydantic v2, `info.data` holds already-validated fields.
        """
        start = info.data.get("start")
        if start is not None and v <= start:
            raise ValueError("end must be after start")
        return v
    
# ----- NEW: resolved (for backend to use) -----
class TimeResolved(BaseModel):
    # strings: ISO8601
    start: str
    end: str
    tz: Optional[str] = "UTC"

TimeSpec = Union[TimeRelative, TimeCalendar, TimeAbsolute, TimeResolved]

# ---- Our intent models (action + params) ----
Explanation = Literal["none", "simple", "verbose"]
SortBy = Literal["ip", "time", "quantity", "score"]
Action = Literal["upload_data", "find_anomalies", "get_output", "rerun"]

# Updated: num_features default to 10, top_n default to 10
class FindAnomaliesIn(BaseModel):
    uid_column: str
    time: Optional[TimeSpec] = None
    top_n: conint(ge=1, le=100) = 10
    num_features: conint(ge=1, le=1024) = 10

class IntentParams(BaseModel):
    top_n: Optional[conint(ge=1, le=100)] = None
    num_features: Optional[conint(ge=1, le=1024)] = None
    time: Optional[TimeSpec] = None
    target_ip: Optional[str] = None
    source_ip: Optional[str] = None          # used as filter in find_anomalies
>>>>>>> frontend
    explanation: Optional[Explanation] = None
    sort_by: Optional[SortBy] = None
    uid_column: Optional[str] = None

class Intent(BaseModel):
    action: Action
    params: IntentParams

