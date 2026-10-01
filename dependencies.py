from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
import os
from passlib.context import CryptContext
from models import User
from jose import jwt, JWTError

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def catch_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session 
        # Yeild funciona parecido a um return, mas ele permite 
        # que a função seja pausada e retomada posteriormente. 
        # Isso é útil para criar geradores ou corrotinas.

        # Yeild works similarly to a return, but it allows
        # that the function to be a paused and resumed later.
        # that is useful for creating generators or coroutines.
    finally:
        session.close()
        # o try executa o código que pode dar erro, 
        # e o finally roda sempre depois dele, com erro ou sem erro.

        # The try executer the code than can give error,
        # and the finally runs always after it, with error or without error.

#-------------------------------------------------------------------------------

def check_token(token: str = Depends(oauth2_schema), session: Session = Depends(catch_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="access denied")
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="invalid access")
    return user
