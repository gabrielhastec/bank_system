
from fastapi import FastAPI

from .routers.account_router import router as account_router
from .routers.auth_router import router as auth_router
from .routers.transaction_router import router as transaction_router

def create_app():
    app = FastAPI(
        title="Banking System API",
        version="0.1.0",
    )

    # Routers
    app.include_router(account_router, prefix="/accounts", tags=["Accounts"])
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(transaction_router, prefix="/transactions", tags=["Transactions"])

    return app

app = create_app()
