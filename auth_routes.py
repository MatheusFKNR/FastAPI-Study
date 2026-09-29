from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def autenticar() :

    return {"message": "You are on the authentication route!"}

# Fuciona igual o order_routes
# functions the same as order_routes