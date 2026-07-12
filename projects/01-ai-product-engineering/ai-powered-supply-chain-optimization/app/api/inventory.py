from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryUpdate,
)
from app.services.inventory import (
    create_inventory_item,
    delete_inventory_item,
    get_inventory_item,
    get_inventory_item_by_sku,
    list_inventory_items,
    list_low_stock_items,
    update_inventory_item,
)


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.post(
    "",
    response_model=InventoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create an inventory item",
)
def create_item(
    inventory_data: InventoryCreate,
    database: Session = Depends(get_db),
) -> InventoryResponse:
    existing_item = get_inventory_item_by_sku(
        database=database,
        sku=inventory_data.sku,
    )

    if existing_item is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An inventory item with SKU '{inventory_data.sku}' already exists.",
        )

    return create_inventory_item(
        database=database,
        inventory_data=inventory_data,
    )


@router.get(
    "",
    response_model=List[InventoryResponse],
    summary="List inventory items",
)
def read_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    database: Session = Depends(get_db),
) -> List[InventoryResponse]:
    return list_inventory_items(
        database=database,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/low-stock",
    response_model=List[InventoryResponse],
    summary="List low-stock inventory items",
)
def read_low_stock_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    database: Session = Depends(get_db),
) -> List[InventoryResponse]:
    return list_low_stock_items(
        database=database,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/sku/{sku}",
    response_model=InventoryResponse,
    summary="Get an inventory item by SKU",
)
def read_item_by_sku(
    sku: str,
    database: Session = Depends(get_db),
) -> InventoryResponse:
    inventory_item = get_inventory_item_by_sku(
        database=database,
        sku=sku,
    )

    if inventory_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with SKU '{sku}' was not found.",
        )

    return inventory_item


@router.get(
    "/{inventory_id}",
    response_model=InventoryResponse,
    summary="Get an inventory item by ID",
)
def read_item(
    inventory_id: int,
    database: Session = Depends(get_db),
) -> InventoryResponse:
    inventory_item = get_inventory_item(
        database=database,
        inventory_id=inventory_id,
    )

    if inventory_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {inventory_id} was not found.",
        )

    return inventory_item


@router.patch(
    "/{inventory_id}",
    response_model=InventoryResponse,
    summary="Update an inventory item",
)
def update_item(
    inventory_id: int,
    inventory_data: InventoryUpdate,
    database: Session = Depends(get_db),
) -> InventoryResponse:
    current_item = get_inventory_item(
        database=database,
        inventory_id=inventory_id,
    )

    if current_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {inventory_id} was not found.",
        )

    update_fields = inventory_data.model_dump(exclude_unset=True)
    new_sku = update_fields.get("sku")

    if new_sku is not None and new_sku != current_item.sku:
        item_with_same_sku = get_inventory_item_by_sku(
            database=database,
            sku=new_sku,
        )

        if item_with_same_sku is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"An inventory item with SKU '{new_sku}' already exists.",
            )

    updated_item = update_inventory_item(
        database=database,
        inventory_id=inventory_id,
        inventory_data=inventory_data,
    )

    if updated_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {inventory_id} was not found.",
        )

    return updated_item


@router.delete(
    "/{inventory_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an inventory item",
)
def delete_item(
    inventory_id: int,
    database: Session = Depends(get_db),
) -> Response:
    deleted = delete_inventory_item(
        database=database,
        inventory_id=inventory_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with ID {inventory_id} was not found.",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)