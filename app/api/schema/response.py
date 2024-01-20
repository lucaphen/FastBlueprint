"""
@author: lucaphen
@date: 20/01/2024

Standardised Response models. 

NOTES: 
- This is integrated into the main.py exception handler.
- Should be used on all endpoints. 
"""
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Union
from datetime import datetime

T = TypeVar('T')

class ResponseModel(Generic[T], BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = "Additional data not available"
    time: Optional[str] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class ErrorResponseModel(BaseModel):
    success: bool
    message: str
    errors: Optional[Union[str, dict]] = None
    time: Optional[str] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')