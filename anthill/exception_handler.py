from fastapi import Request
from fastapi.responses import JSONResponse


async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": f"error! {str(exc)}"},
        )
