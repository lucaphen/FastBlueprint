from pydantic import BaseModel
from datetime import date

class Contract(BaseModel):
    id: str
    user: str
    amount: float
    date: date
