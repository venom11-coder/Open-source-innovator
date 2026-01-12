from pydantic import BaseModel
from typing import  List


# strctured output for items inputted and number of combinations at each time
class Combinations(BaseModel):

    items: List[str]
    weight_step: int = 1 
    size: int


