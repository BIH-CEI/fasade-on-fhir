from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from redcaponfhir.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config.auth.secret_key, algorithms=[config.auth.algorithm])
        return payload
    except JWTError:
        raise credentials_exception


def validate_token(token: Dict[str, Any] = Depends(get_token)) -> bool:
    return True
