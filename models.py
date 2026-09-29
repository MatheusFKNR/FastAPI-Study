# Imports e configuração do banco de dados - Imports and the database configuration

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

# Cria a conexão com o banco de dados - creates the connection with the database
db = create_engine('sqlite:///database.db')

# Cria a base do banco de dados - creates the database base
Base = declarative_base()

#-------------------------------------------------------------------------------

#Usuários - Users
class User(Base):

    # __tablename__ é o nome da tabela no banco de dados - __tablename__ is the namen of the table in the database

    __tablename__ = 'users'
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String(40), nullable=False)
    email = Column("email", String(100), unique=True, nullable=False)
    password = Column("password", String(100), nullable=False)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self,name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


#-------------------------------------------------------------------------------

#Pedidos - orders
class Order(Base):
    __tablename__ = 'orders'

    STATUS_ORDERS = {
        ("PENDING", "PENDING"),
        ("CANCELED", "CANCELED"),
        ("FINISHED", "FINISHED"),
    }

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    # status = Column("status", String, nullable=False) 
    status = Column("status", ChoiceType(choices = STATUS_ORDERS))
    user = Column("user", Integer, ForeignKey('users.id'), nullable=False)
    price = Column("price", Float, nullable=False)

    # Itens (ainda não foi criado - hasn't been made yet)=

    def __init__(self, status, user, price):
        self.status = status
        self.user = user
        self.price = price

    
#Itens do pedido (pizza) - order items (pizza)
class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    unitary_price = Column("unitary_price", Float)
    order = Column("order_id", Integer, ForeignKey('orders.id'), nullable=False)

    def __init__(self, quantity, flavor, size, unitary_price, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unitary_price = unitary_price
        self.order = order


#Visão geral
# O código define três tabelas de um sistema de pedidos de pizzaria 
# usando o ORM do SQLAlchemy (estilo clássico).
# Cada classe vira uma tabela, e cada Column vira uma coluna.

# Overview
# the code defines three tables of a pizza ordering system
# using the ORM of SQLAlchemy (classic style).
# Each class becomer a table, and each Column becomes a column.