from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..utils import standard_response

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)

from fastapi.responses import JSONResponse

@router.post("/{store_id}", response_model=dict, status_code=status.HTTP_201_CREATED)
def add_inventory(store_id: int, inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=standard_response(success=False, error="Store not found")
        )

    product = db.query(models.Product).filter(models.Product.id == inventory.product_id).first()
    if not product:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=standard_response(success=False, error="Product not found")
        )

    # Check if inventory entry already exists
    existing_inv = db.query(models.Inventory).filter(
        models.Inventory.store_id == store_id,
        models.Inventory.product_id == inventory.product_id
    ).first()

    if existing_inv:
        existing_inv.quantity += inventory.quantity
        db_inv = existing_inv
    else:
        db_inv = models.Inventory(**inventory.model_dump(), store_id=store_id)
        db.add(db_inv)

    try:
        db.commit()
        db.refresh(db_inv)
        return standard_response(success=True, data=schemas.InventoryOut.model_validate(db_inv).model_dump())
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=standard_response(success=False, error=str(e))
        )


@router.put("/{store_id}/{product_id}", response_model=dict)
def update_inventory(store_id: int, product_id: int, inventory: schemas.InventoryUpdate, db: Session = Depends(get_db)):
    inv = db.query(models.Inventory).filter(
        models.Inventory.store_id == store_id,
        models.Inventory.product_id == product_id
    ).first()

    if not inv:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=standard_response(success=False, error="Inventory record not found")
        )

    inv.quantity = inventory.quantity
    try:
        db.commit()
        db.refresh(inv)
        return standard_response(success=True, data=schemas.InventoryOut.model_validate(inv).model_dump())
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=standard_response(success=False, error=str(e))
        )
