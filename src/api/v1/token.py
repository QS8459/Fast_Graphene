from fastapi import (
    APIRouter,
    Request,
    Response,
    status
)
from src.core.service.authentication import generate_token
from uuid import uuid4

token_api: APIRouter = APIRouter(prefix="/token", tags=["token"])


@token_api.post(
    '/',
    status_code=status.HTTP_200_OK
)
async def give_token(
    request: Request,
    response: Response
):
    anonymous_user_uid = f"{str(uuid4())}"
    token = generate_token(
        {
            "guid": anonymous_user_uid,
        },
        exp_time=1800
    )
    response.headers.update(
        {
            "Set-Cookie": f"access_token={token}"
        }
    )
    return 0

