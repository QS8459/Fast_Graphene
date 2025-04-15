import jwt
from datetime import (
    datetime,
    timedelta,
    timezone
)
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import (
    HTTPException,
    status
)
from src.conf.settings import settings
from src.conf.log import logger

o2auth_scheme = OAuth2PasswordBearer(tokenUrl='/graphql', scheme_name="jwt")


def generate_token(
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


def get_user(
        token: str
):
    try:

        decoded = jwt.decode(
            token,
            algorithms=[settings.token_alg],
            key=settings.token_key,
        )
        time_diff = (datetime.now(timezone.utc).timestamp() - decoded.get("exp")) / 60
        if time_diff > 30:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Timeout",
                headers={"Authentication": "Bearer"}
            )
        return {
            "guid": decoded.get('guid'),
            "username": decoded.get('username')
        }

    except Exception as e:
        logger.debug(f"Exception, {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"Authentication": "Bearer"}
        )
