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
# TODO: add a timestamp, uid_column change to columns_name: uid, timestamp, souce_ip(ho e identify the anomalies) (the header names in the csv);
class IntentParams(BaseModel):
    top_n: Optional[conint(ge=1, le=100)] = None
    num_features: Optional[conint(ge=1, le=1024)] = None
    time_range: Optional[TimeRange] = None # sho me anomalies elated to this ip, 
    target_ip: Optional[str] = None # sho me anomalies elated in this time ange 
    explanation: Optional[Explanation] = None
    sort_by: Optional[SortBy] = None 
    uid_column: Optional[str] = None

class Intent(BaseModel):
    action: Action
    params: IntentParams

