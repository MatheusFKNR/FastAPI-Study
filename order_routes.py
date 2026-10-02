#we import APIRouer from fastapi to create routes
#importamos do fastapi o APIRouter para criar rotas

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import catch_session, check_token
from dependencies import sessionmaker
from schemas import SchemaOrder, orderItemSchema, ResponseSchemaOrder
from models import Order, User, orderItem
from typing import List

# Criamos uma variavel chamada order_router que recebe o APIRouter, com o prefixo
# /orders e a tag orders, API Router é uma forma de criar rotas no FastAPI,
# e o prefixo é a parte da URL que será usada para acessar essas rotas.

#we create a variable called order_router that receives the APIRouter, with the prefix
# /orders and the tag orders, API Router is a way of creatig routes in FastAPI,
# and the prefx is the part of the URL that will used to acess these routes.

order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(check_token)])

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

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(catch_session), user: User = Depends(check_token)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code = 400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permission for make this modification")
    order.status = "CANCELED"
    session.commit()
    return{
        "mensage": f"Order number : {order_id} successfully canceled",
        "order" : order
    }

@order_router.get("/list")
async def list_orders(session: Session = Depends(catch_session), user: User = Depends(check_token)):
    if user.admin == False:
        raise HTTPException(status_code=401, detail="You don't have permission for make this operation")
    else :
        orders = session.query(Order).all()
        return{
            "orders": orders        }


@order_router.post("/order/add-item/{order_id}")
async def add_item_order(order_id:int, 
                         item_order_shema : orderItemSchema, 
                         session: Session = Depends(catch_session), 
                         user: User = Depends(check_token)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="order does not exist")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permission for make this operation")
    order_item = orderItem( quantity=item_order_shema.quantity,
                            flavor=item_order_shema.flavor,
                            size=item_order_shema.size,
                            unitary_price=item_order_shema.unitary_price,
                            order=order_id 
)   
    session.add(order_item)
    session.flush()  # Garante que o novo item é enviado ao banco antes de atualizar o preço
    session.refresh(order)
    order.calculate_price()
    session.commit()
    return{
        "mesage": "item created successfully",
        "item_id": order_item.id,
        "unit_price": order.price
    }


@order_router.post("/order/remove-item/{order_id_item}")
async def remove_item_order(order_id_item:int, 
                            session: Session = Depends(catch_session), 
                            user: User = Depends(check_token)):
    # Busca o item na tabela 'orderItem' (em vez de buscar na tabela Order)
    order_item = session.query(orderItem).filter(orderItem.id == order_id_item).first()
    if not order_item:
        raise HTTPException(status_code=400, detail="item on order does not exist")

    # Busca a Order referente ao item encontrado
    order = session.query(Order).filter(Order.id == order_item.order).first()
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permission for make this operation")

    session.delete(order_item)
    session.flush()  # Remove o item da sessão do banco antes do recálculo
    
    if order:
        session.refresh(order)
        order.calculate_price()

    session.commit()
    return{
        "mesage": "item successfully removed",
        "quantity_order_item": len(order.items),
        "order": order_item.order
    }

# finish a order


@order_router.post("/order/finished/{order_id}")
async def finish_order(order_id: int, session: Session = Depends(catch_session), user: User = Depends(check_token)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code = 400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permission for make this modification")
    order.status = "FINISHED"
    session.commit()
    return{
        "mensage": f"Order number : {order_id} successfully finished",
        "order" : order
    }

# view an order

@order_router.get("/order/{order_id}")
async def view_order(order_id: int, session: Session = Depends(catch_session), user: User = Depends(check_token)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code = 400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You don't have permission for make this modification")
    #return {
    #    "quantity_item_order": len(order.items),
    #   "order": order
    #}
    return order

# view all of a user's orders

@order_router.get("/list/user_orders/{user_id}", response_model=List[ResponseSchemaOrder])
async def orders_by_user(
    user_id: int, 
    session: Session = Depends(catch_session), 
    user: User = Depends(check_token)
):
    if not user.admin:
        raise HTTPException(status_code=401, detail="You don't have permission to make this operation")

    orders = session.query(Order).filter(Order.user == user_id).all()
    return {"orders": orders}