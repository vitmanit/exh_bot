from pydantic import BaseModel, Field, validator, field_validator, ConfigDict
from typing import List, Optional, Annotated


class MonitoringBase(BaseModel):
    name: str = Field(min_length=5, max_length=50, description="Name of the monitoring")
    link: str = Field(min_length=5, max_length=50, description="Link to the monitoring")
    can_do: bool = Field(default=False, description="Whether the monitoring can do")
    description: str = Field(min_length=5, max_length=50, description="Description of the monitoring")
    exchanger_id: int = Field(description="Exchange ID")

    model_config = ConfigDict(from_attributes=True)

class MonitoringCreate(MonitoringBase):
    pass

class MonitoringResponse(MonitoringBase):
    pass

class MonitoringUpdate(MonitoringBase):
    name: Optional[str] = None
    link: Optional[str] = None
    can_do: Optional[bool] = None
    description: Optional[str] = None
    exchanger_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, extra='ignore')
