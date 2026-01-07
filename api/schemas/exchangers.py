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
    workers: str = Field(min_length=1, max_length=35, description='Работники')

    model_config = ConfigDict(from_attributes=True)


class ExchangerResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class ExchangerUpdate(ExchangerCreate):
    name: Optional[str] = None
    in_work: Optional[bool] = None
    automated_bot: Optional[bool] = None
    making_orders: Optional[bool] = None
    plan_best_ru: Optional[int] = None
    plan_best_eng: Optional[int] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra='ignore'  # Игнорирует лишние поля в JSON
    )

