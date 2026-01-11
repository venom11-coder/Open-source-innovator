from pydantic import BaseModel
from typing import Annotated, List, Literal, Optional

# structured output for csv file
class Output_Csv(BaseModel):

    items: List[str]
    size: int
    combinations: List[str]
    id: str
    created_at: str
    filepath: str 