from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from datetime import datetime
from app.api.endpoints import transactions, contracts, authentication
from app.api.schema import ErrorResponseModel, ResponseModel
from app.core.database import Base, engine

app = FastAPI()

# app configurations
Base.metadata.create_all(bind=engine)

# exception handlers
@app.exception_handler(RateLimitExceeded) # exception handler: rate limiter
async def rate_limit_exceeded_handler(request, exc):
    return Response(str(exc), status_code=429)

@app.exception_handler(HTTPException) # exception handler: HTTP exceptions
async def http_exception_handler(request: Request, exception: HTTPException):
    error_response = ErrorResponseModel(
        success=False,
        message=str(exception.detail),
        errors='Error Code: ' + str(exception.status_code)
    )
    return JSONResponse(status_code=exception.status_code, content=error_response.model_dump())
    

# router configuration
app.include_router(transactions, prefix="/transactions")
app.include_router(contracts, prefix="/contracts")
app.include_router(authentication, prefix="/auth")

# api health check
@app.get('/', response_model=ResponseModel[str])
def health_check(): 
    return ResponseModel(success=True, message="Server is running")
