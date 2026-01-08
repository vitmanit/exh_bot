from pydantic import BaseModel, Field, validator, field_validator, ConfigDict
from typing import List, Optional, Annotated


class PlanBase(BaseModel):
    exchanger_id: int = Field(..., description='Exchanger ID')
    monitoring_id: int = Field(..., description='Monitoring ID')
    plan_per_day: int = Field(..., description='Plan per day')

    model_config = ConfigDict(from_attributes=True)


class PlanResponse(PlanBase):
    id: int = Field(..., description='Plan ID')



class PlanCreate(PlanBase):
    pass


class PlanUpdate(PlanBase):
    exchanger_id: Optional[int] = Field(None, description='Exchanger ID')
    monitoring_id: Optional[int] = Field(None, description='Monitoring ID')
    plan_per_day: Optional[int] = Field(None, description='Plan per day')