#we import APIRouer from fastapi to create routes
#importamos do fastapi o APIRouter para criar rotas

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import catch_session
from dependencies import sessionmaker
from schemas import SchemaOrder
from models import Order

# Criamos uma variavel chamada order_router que recebe o APIRouter, com o prefixo
# /orders e a tag orders, API Router é uma forma de criar rotas no FastAPI,
# e o prefixo é a parte da URL que será usada para acessar essas rotas.

#we create a variable called order_router that receives the APIRouter, with the prefix
# /orders and the tag orders, API Router is a way of creatig routes in FastAPI,
# and the prefx is the part of the URL that will used to acess these routes.

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
async def orders():
    return {"message": "You are on the orders route!"}

# Esse bloco cria um agrupador de rotas para pedidos
# (/orders, documentado sob a tag "orders") e registra nele uma rota GET /orders/ 
# que responde com a mensagem "You are on the orders route!".

# This block creates a route group for orders
# (/orders, documented under the tag "orders") and registers a GET /orders/ route
# that responds with the message "You are on the orders route!".

@order_router.post("/")
async def create_order(schema_order: SchemaOrder, session: Session = Depends(catch_session)):
    new_order = Order(user=schema_order.user_id)
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return {"message": "Order created successfully", "order_id": new_order.id}