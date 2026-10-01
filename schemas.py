# Este código define modelos de dados (Schemas) usando a biblioteca Pydantic no Python
# This code defines data models (schemas) using the Pydantic library in Python

# Garante que os dados que entram ou saem da aplicação estejam no formato ---- # Makes sure the data going in or out of the app is in the right format
# e no tipo corretos (como números, textos ou booleanos). --- # and type (like numbers, text, or booleans).


from pydantic import BaseModel
from typing import Optional

# Define a estrutura esperada para dados de um usuário:
# Define the expected structure for user data:  

class UserSchema(BaseModel):
    name:str
    email:str
    password:str
    active: Optional[bool] = False
    admin: Optional[bool] = False
 
    class Config:
        from_attributes = True

class SchemaOrder(BaseModel):
    user_id: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email:str
    password: str

    class Config:
        from_attributes = True