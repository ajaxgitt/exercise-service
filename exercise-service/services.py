from decouple import config
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import HTTPException, Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


def verify_token(token:str =Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, config('SECRET_KEY'), algorithms=[config('ALGORITHM')])
        id_user: str = payload.get("sub")
        if id_user is None:
            raise HTTPException(status_code=403, detail="token is invalid or expired")
        return payload 
    except JWTError:
        raise HTTPException(status_code=403, detail="token is invalid or expired")