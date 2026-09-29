# Creating the FastAPI - Criando o fastAPI  
from fastapi import FastAPI

app = FastAPI()

#-------------------------------------------------------------------------------

# Import the files for the main - importando os arquivos para o main

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

# para rodar o nosso código, executar no terminal : uvicorn main:app --reload

# endpoint:
# dominio.com/order

# Rest APIs
# Get - leitura/pegar
# Post - enviar/criar
# Put/patch - edição
# Delete - deletar