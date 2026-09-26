from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any
from datetime import datetime

class RetailerBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class RetailerCreate(RetailerBase):
    pass

class RetailerOut(RetailerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True


class StoreBase(BaseModel):
    name: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class StoreCreate(StoreBase):
    pass

class StoreOut(StoreBase):
    id: int
    retailer_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    price: float

class ProductCreate(ProductBase):
    embedding: Optional[List[float]] = None

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    # typically don't expose embeddings in standard output

    class Config:
        orm_mode = True
        from_attributes = True


class InventoryBase(BaseModel):
    quantity: int

class InventoryCreate(InventoryBase):
    product_id: int

class InventoryUpdate(InventoryBase):
    pass

class InventoryOut(InventoryBase):
    id: int
    store_id: int
    product_id: int
    last_updated: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class InventoryDetailOut(InventoryOut):
    product: ProductOut

class SearchResultOut(BaseModel):
    product: ProductOut
    distance: Optional[float] = None
    store_id: int
    quantity: int

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    size: int
