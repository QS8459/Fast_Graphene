from fastapi import (
    Request,
    HTTPException,
    Depends,
    status
)
from src.conf.log import logger


async def provide_session(
        request: Request,
        call_next,
):
    logger.info("Proved session")
    try:
        result = await call_next(request)
        return result
    except Exception as e:
        raise e
        # raise HTTPException(
        #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     detail="Internal Server Error"
        # )