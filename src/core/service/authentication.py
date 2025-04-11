import jwt
from datetime import (
    datetime,
    timedelta,
    timezone
)
from fastapi.security.oauth2 import OAuth2PasswordBearer
from src.conf.di import di
from src.conf.settings import settings

o2auth_scheme = OAuth2PasswordBearer(tokenUrl='/graphql', scheme_name="jwt")


async def generate_token(
        data: dict,
        exp_time
):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=exp_time)
    to_encode.update({"exp": expire})

    return jwt.encode(
        key=settings.token_key,
        algorithm=settings.token_alg,
        payload=to_encode
    )

