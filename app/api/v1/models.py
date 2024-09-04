from pydantic import BaseModel
from typing import List, Any


class Param(BaseModel):
    column_name: str
    value: Any


class DynamicQueryRequest(BaseModel):
    db_schema: str
    func_name: str
    limit: int
    params: List[Param]
