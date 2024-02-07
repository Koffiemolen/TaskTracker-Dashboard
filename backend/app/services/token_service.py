import jwt
from datetime import datetime, timedelta
from os import getenv
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_access_token(data: dict, expires_delta: timedelta = None):
    print(f"Creating access token for {data}")
    logger.info(f"Creating access token for {data}")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, getenv("JWT_SECRET_KEY"), algorithm=getenv("JWT_ALGORITHM"))
    return encoded_jwt
