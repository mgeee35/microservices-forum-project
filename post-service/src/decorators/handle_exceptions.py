import asyncio
import traceback
from functools import wraps

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as e:
            return JSONResponse(
                success=False,
                reasonPhrase=str(e),
                statusCode=status.HTTP_400_BAD_REQUEST,
                data=None
            )
        except ValueError as e: 
            return JSONResponse(
                success=False,
                reasonPhrase=str(e),
                statusCode=status.HTTP_400_BAD_REQUEST,
                data=None
            )
        except Exception as e:
            traceback.print_exc()
            return JSONResponse(
                success=False,
                reasonPhrase=str(e),
                statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=None
            )
    return wrapper
