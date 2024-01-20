"""
    File: contracts.py
    Type: route
    Explanation: This route facilitates CRUD operations for the Contracts Service.
    Author: @lucaphen Github
"""
# dependencies
from fastapi import APIRouter, Request
from app.api.schema.response import ResponseModel, ErrorResponseModel
from app.api.schema.contracts import Contract
from app.core.dependencies import limiter
from app.core.config import (
    RATE_LIMIT # 10/minute
)
# development dependencies
from datetime import date

# Router initialization
router = APIRouter()

@router.get('/{contract_id}', response_model=ResponseModel[Contract])
@limiter.limit(RATE_LIMIT)
async def get_contract(
    request: Request, # requirement for slowapi
    contract_id: str,
): 
    # NOTE: dummy contract information 
    contract = Contract(
        id=contract_id,
        user=request.headers.get('user-agent'),
        amount=15000.00,
        date=date.today()
    )
    return ResponseModel(success=True, message="Get Contract", data=contract.model_dump())

