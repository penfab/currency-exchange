from fastapi import FastAPI


def serve_api():
    from currency_exchange.router import router as currency_exchange_router

    
    api = FastAPI()
    api.include_router(currency_exchange_router, prefix="/currency_exchange")
    
    return api
