from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, validator, Field


class ServerStatusSchema(BaseModel):
    active_user_in_5m: int = None
    active_user_in_1h: int = None
    active_user_in_1d: int = None
    is_chatbot_busy: bool = None
    chatbot_waiting_count: int = None


class SystemInfo(BaseModel):
    startup_time: float
    total_user_count: int
    total_conversation_count: int
    valid_conversation_count: int


class LogFilterOptions(BaseModel):
    max_lines: int = 100
    exclude_keywords: list[str] = None

    @validator("max_lines")
    def max_lines_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("max_lines must be positive")
        return v


datetime.now().astimezone()


class RequestStatsAggregationID(BaseModel):
    start_time: datetime
    route_path: str
    method: str


class RequestStatsAggregation(BaseModel):
    id: RequestStatsAggregationID = Field(None, alias="_id")  # 起始时间
    count: int  # 时间间隔内的请求数量
    user_ids: list[Optional[int]] = None  # 用户ID列表
    avg_elapsed_ms: Optional[float]

    class Config:
        json_encoders = {
            datetime: lambda d: d.astimezone(tz=timezone.utc)
        }