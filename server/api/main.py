from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import (
    customers,
    phone_numbers,
    phone_ranges,
)

app = FastAPI()
app.include_router(customers.router)
app.include_router(phone_numbers.router)
app.include_router(phone_ranges.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
