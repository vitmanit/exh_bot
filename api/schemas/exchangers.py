from fastapi import Query
from pydantic import BaseModel, Field, validator, field_validator, ConfigDict
from typing import List, Optional, Annotated


class ExchangerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, description='Введите название обменника')
    in_work: bool = Field(default=True, description='В работе?')
    automated_bot: bool = Field(default=True, description='Автоматизирован?')
    making_orders: bool = Field(default=True, description='Принимает заказы?')
    plan_best_ru: int = Field(ge=0, description='План на день RU')
    plan_best_eng: int = Field(ge=0, description='План на день RU')
    description: str = Field(min_length=1, max_length=150, description='Описание для работы с обменником')

    model_config = ConfigDict(from_attributes=True)


class ExchangerResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class ExchangerUpdate(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=100, description='Введите название обменника'), Query()]] = None
    in_work: Optional[Annotated[bool, Field(default=True, description='В работе?'), Query()]] = None
    automated_bot: Optional[Annotated[bool, Field(default=True, description='Автоматизирован?'), Query()]] = None
    making_orders: Optional[Annotated[bool, Field(default=True, description='Принимает заказы?'), Query()]] = None
    plan_best_ru: Optional[Annotated[int, Field(ge=0, description='План на день RU'), Query()]] = None
    plan_best_eng: Optional[Annotated[int, Field(ge=0, description='План на день ENG'), Query()]] = None
    description: Optional[Annotated[str, Field(min_length=1, max_length=150, description='Описание для работы с обменником'), Query()]] = None