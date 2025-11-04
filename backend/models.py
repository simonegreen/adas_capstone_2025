# models.py (time spec section)
from enum import IntEnum
from pydantic import BaseModel, conint, field_validator, ConfigDict
from typing import Optional, Union, Literal
from datetime import datetime

class URel(IntEnum):
    HOUR = 1; DAY = 2; WEEK = 3; MONTH = 4

class UCal(IntEnum):
    DAY = 2; WEEK = 3; MONTH = 4; QUARTER = 5; YEAR = 6

class TimeRelative(BaseModel):
    model_config = ConfigDict(use_enum_values=True)  # serialize enums as ints
    kind: Literal["relative"] = "relative"
    unit: URel                 # 1=hour,2=day,3=week,4=month
    n: int                     # signed periods; -1=past 1, +2=next 2
    round: conint(ge=0, le=1) = 0  # 0=rolling, 1=snap boundary
    tz: str = "America/New_York"

    @field_validator("n")
    @classmethod
    def non_zero(cls, v):
        if v == 0:
            raise ValueError("n cannot be 0")
        return v

class TimeCalendar(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    kind: Literal["calendar"] = "calendar"
    unit: UCal                 # 2=day,3=week,4=month,5=quarter,6=year
    offset: int = -1           # -1=previous period, 0=this, +1=next
    tz: str = "America/New_York"
    week_start: Optional[conint(ge=0, le=1)] = None  # 0=sunday, 1=monday

    @field_validator("week_start")
    @classmethod
    def require_ws_for_week(cls, v, values):
        if values.get("unit") == UCal.WEEK and v is None:
            raise ValueError("week_start is required when unit=WEEK")
        return v

class TimeAbsolute(BaseModel):
    kind: Literal["absolute"] = "absolute"
    start: datetime
    end: datetime
    tz: Optional[str] = None

    @field_validator("end")
    @classmethod
    def end_after_start(cls, v, values):
        if "start" in values and v <= values["start"]:
            raise ValueError("end must be after start")
        return v

TimeSpec = Union[TimeRelative, TimeCalendar, TimeAbsolute]

# NOTE: sort by score is suspended for now
# ---- Our intent models (action + params) ----
Explanation = Literal["none", "simple", "verbose"]
SortBy = Literal["ip", "time", "quantity", "score"]
Action = Literal["upload_data", "find_anomalies", "get_output", "rerun", "reset"]

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
    explanation: Optional[Explanation] = None
    sort_by: Optional[SortBy] = None
    uid_column: Optional[str] = None

class Intent(BaseModel):
    action: Action
    params: IntentParams

