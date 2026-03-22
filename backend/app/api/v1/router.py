"""
API v1 Router
Aggregates all endpoint routers
"""
from fastapi import APIRouter
from app.api.v1.endpoints import ingredients, products, scan, admin, payments, auth

api_router = APIRouter()

api_router.include_router(
    ingredients.router,
    prefix="/ingredients",
    tags=["ingredients"]
)

api_router.include_router(
    products.router,
    prefix="/products",
    tags=["products"]
)

api_router.include_router(
    scan.router,
    prefix="/scan",
    tags=["scan"]
)

api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"]
)

api_router.include_router(
    payments.router,
    prefix="/payments",
    tags=["payments"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)
