from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import retailer, store, product, inventory, search
from .utils import standard_response

app = FastAPI(
    title="NearShop API",
    description="AI Powered Product and Inventory Search for Local Retailers",
    version="1.0.0"
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler setup omitted to allow FastAPI defaults (like RequestValidationError/HTTPException)

# Include Routers
app.include_router(retailer.router)
app.include_router(store.router)
app.include_router(product.router)
app.include_router(inventory.router)
app.include_router(search.router)

@app.get("/")
def read_root():
    return standard_response(success=True, data={"message": "Welcome to NearShop API"})
