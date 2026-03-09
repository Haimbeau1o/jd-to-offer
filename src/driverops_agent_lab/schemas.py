from __future__ import annotations

from pydantic import BaseModel, Field


class DriverProfile(BaseModel):
    driver_id: str
    city: str
    tier: str
    vehicle_type: str
    preferred_hours: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class TripStats(BaseModel):
    driver_id: str
    today_income: float
    yesterday_income: float
    completion_rate: float
    acceptance_rate: float
    peak_zone: str
    top_hours: list[str] = Field(default_factory=list)


class Campaign(BaseModel):
    campaign_id: str
    city: str
    title: str
    segment: str
    reward: str
    window: str


class ToolTrace(BaseModel):
    tool_name: str
    arguments: dict[str, str] = Field(default_factory=dict)
    result_summary: str


class ChatRequest(BaseModel):
    driver_id: str
    city: str = "beijing"
    query: str


class AgentResponse(BaseModel):
    driver_id: str
    city: str
    intent: str
    answer: str
    recommendations: list[str] = Field(default_factory=list)
    tool_trace: list[ToolTrace] = Field(default_factory=list)
    memory_snapshot: list[str] = Field(default_factory=list)
