from pydantic import BaseModel
from typing import Dict, List

class StatsResponse(BaseModel):
    total_processes: int
    total_lanes: int
    total_tasks: int
    task_types: Dict[str, int]
    total_gateways: int
    gateway_types: Dict[str, int]
    total_events: int
    event_types: Dict[str, int]
    total_flows: int
    flow_types: Dict[str, int]
    total_subprocesses: int
    total_data_objects: int
    total_data_stores: int
    has_error_handling: bool
    has_compensation: bool
    complexity_score: int


class AnalysisResponse(BaseModel):
    stats: StatsResponse
    suggestions: List[str]
