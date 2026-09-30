# Creating the FastAPI - Criando o fastAPI  
from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#-------------------------------------------------------------------------------

# importando os arquivos para o main - Import the files for the main 

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# para rodar o nosso código, executar no terminal : uvicorn main:app --reload
# for running our code, run in the terminal: uvicorn main:app --reload

# endpoint:
# dominio.com/order

# Rest APIs
# Get - leitura/pegar - reading/get
# Post - enviar/criar - send/create
# Put/patch - edição - edit
# Delete - deletar - delete 

