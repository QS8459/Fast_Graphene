from fastapi import (
    Request,
    HTTPException,
    Depends,
    status
)
from src.conf.log import logger
from src.core.service.authentication import (
    get_user
)


async def provide_session(
        request: Request,
        call_next,
):
    logger.info("Proved session")
    try:
        result = await call_next(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

    return result


async def authentication_middleware(
        request: Request,
        call_next
):
    try:
        if request.url.path in ['/graphql']:
            logger.info("Authentication Middleware")
            auth_header = request.headers.get("Authentication")
            token = auth_header.split(' ')[1]
            user = get_user(token)
            if user:
                logger.info("User is fine")
                result = await call_next(request)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bad Request"
                )
        else:
            result = await call_next(request)
    except Exception as e:
        pass
        # raise e

    return result
