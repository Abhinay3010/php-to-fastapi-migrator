from fastapi import FastAPI
from fastapi_app.routes import generated

app = FastAPI()

app.include_router(generated.router)
