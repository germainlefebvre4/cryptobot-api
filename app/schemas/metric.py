from typing import Optional

from pydantic import BaseModel


class MetricBase(BaseModel):
    count: int

class MetricUserCount(MetricBase):
    status: str
