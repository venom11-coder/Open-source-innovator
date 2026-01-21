from pydantic import BaseModel
from typing import  List

# structured output for csv file
class Output_Csv(BaseModel):

    items: List[str] # input items
    size: int # size requested
    combinations: List[str] # output combinations
    combos: str # time the combos were generated in with a other details