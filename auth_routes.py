from fastapi import APIRouter, Depends, HTTPException, status
from models import User
from dependencies import catch_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    return {"message": "You are on the authentication route!"}


@auth_router.post("/create_account", status_code=status.HTTP_201_CREATED)
async def create_account(user_schema: UserSchema, session = Depends(catch_session)):
    # 1. Verificar se o usuário já existe
    # verify if the user already exists
    user = session.query(User).filter(User.email == user_schema.email).first()

    if user:
        # Lança erro HTTP 400 em vez de retornar status 200
        # Raises HTTP 400 error instead of returning status 200
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists."
        )

    # 2. Criptografar a senha
    # Crypt the password
    encrypted_password = bcrypt_context.hash(user_schema.password)

    # 3. Criar a instância passando os campos nomeados
    # Create the isntance passing the named fields
    new_user = User(
        name=user_schema.name,
        email=user_schema.email,
        password=encrypted_password
    )

    # 4. Salvar e confirmar no banco
    # save and commit to the database
    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # Recarrega o objeto gravado no banco
                               # Reloads the object saved in the database

    return {"message":  f"User created successfully {user_schema.email}"}