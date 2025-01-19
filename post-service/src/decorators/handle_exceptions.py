import asyncio
import traceback
from functools import wraps

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "reasonPhrase": str(e.detail),
                    "statusCode": e.status_code,
                    "data": None,
                },
            )
        except ValueError as e:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "success": False,
                    "reasonPhrase": str(e),
                    "statusCode": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                },
            )
        except Exception as e:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "reasonPhrase": str(e),
                    "statusCode": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "details": traceback.format_exc(),
                },
            )

    return wrapper
