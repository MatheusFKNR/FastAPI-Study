from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt  # pip install python-jose
from sqlalchemy.orm import Session
from models import User
from schemas import UserSchema

#-------------------------------------------------------------------------------

# A chave secreta deve vir de uma variável de ambiente, nunca fixa no código
# The secret key must come from an environment variable, never hardcoded
# (agora ela é lida uma única vez em dependencies.py e importada aqui)
from dependencies import (
    catch_session,
    check_token,
    bcrypt_context,
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

#-------------------------------------------------------------------------------

auth_router = APIRouter(prefix="/auth", tags=["auth"])

#-------------------------------------------------------------------------------

# Criação do token

def create_token(user_id, token_duration=None):
    if token_duration is None:
        token_duration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expiration_date = datetime.now(timezone.utc) + token_duration
    dic_info = {"sub": str(user_id), "exp": expiration_date}  # sub precisa ser string
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

#-------------------------------------------------------------------------------

# Checagem do token

# O check_token fica em dependencies.py e é importado acima.
# NÃO redefina ele aqui, senão o botão Authorize some.
# Verificar se o token é valido - check if the token is valided
# E extrair o id do usuário do token - and extract the user id of from the token

#-------------------------------------------------------------------------------

# Autenticar usuário

def authenticate_user(email, password, session):
    # Sempre que for buscar algo no DB utilizar o session.query --- # Whenever you need to grab something from the DB, use session.query
    # e passar a tabela que esta fazendo a busca dentro dos () --- # and pass the table that is doing the search inside the ()
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None
    elif not bcrypt_context.verify(password, user.password):
        # vai verificar se a senha é igual a senha criptografada do usuario
        # go verify if the password matches the user's encrypted password
        return None

    return user

#-------------------------------------------------------------------------------

# As rotas usam "def" (e não "async def") porque as chamadas ao banco são síncronas
# The routes use "def" (not "async def") because the DB calls are synchronous
@auth_router.get("/")
def home():
    return {"message": "You are on the authentication route!"}

#-------------------------------------------------------------------------------

@auth_router.post("/create_account", status_code=status.HTTP_201_CREATED)
def create_account(user_schema: UserSchema, session: Session = Depends(catch_session)):
    # 1. Verificar se o usuário já existe # verify if the user already exists
    user = session.query(User).filter(User.email == user_schema.email).first()

    if user:
        # Lança erro HTTP 409 em vez de retornar status 200 # Raises HTTP 409 error instead of returning status 200
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists."
        )

    # 2. Criptografar a senha # Crypt the password
    encrypted_password = bcrypt_context.hash(user_schema.password)

    # 3. Criar a instância passando os campos nomeados # Create the isntance passing the named fields
    new_user = User(
        name=user_schema.name,
        email=user_schema.email,
        password=encrypted_password
    )

    # 4. Salvar e confirmar no banco
    # save and commit to the database
    session.add(new_user)
    session.commit()
    session.refresh(new_user)  # Recarrega o objeto gravado no banco # Reloads the object saved in the database

    return {"message": f"User created successfully {user_schema.email}"}

#-------------------------------------------------------------------------------

# Login -> email and password -> token JWT (Json Web Token) {random token key}

# OAuth2PasswordRequestForm recebe form data (é o que o botão Authorize envia)
# O campo "username" do formulário recebe o e-mail
@auth_router.post("/login-form")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(catch_session)):
    user = authenticate_user(form_data.username, form_data.password, session)

    # Mesma mensagem para usuário inexistente e senha errada, assim ninguém descobre quais e-mails existem
    # Same message for missing user and wrong password, so nobody can discover which emails exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or credentials invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_token(user.id)
    refresh_token = create_token(user.id, token_duration=timedelta(days=7))

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

#-------------------------------------------------------------------------------

@auth_router.get("/refresh")
def use_refresh_token(user: User = Depends(check_token)):
    access_token = create_token(user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }