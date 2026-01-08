from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Union, List, Any
from pydantic import ConfigDict

class PyObjectId(str):
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return core_schema.schema_json_or_python_of(str)


class MongoBase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    id: Union[PyObjectId, str] = Field(alias="_id", default=None)


class Exchanger(MongoBase):
    name: str
    url: str
    sites: List[str] = []
