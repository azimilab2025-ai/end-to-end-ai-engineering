from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import InventoryItem
from app.schemas.inventory import InventoryCreate, InventoryUpdate


def create_inventory_item(
    database: Session,
    inventory_data: InventoryCreate,
) -> InventoryItem:
    """Create and persist a new inventory item."""

    existing_item = get_inventory_item_by_sku(
        database=database,
        sku=inventory_data.sku,
    )

    if existing_item is not None:
        raise ValueError(
            f"An inventory item with SKU '{inventory_data.sku}' already exists."
        )

    inventory_item = InventoryItem(
        **inventory_data.model_dump()
    )

    database.add(inventory_item)
    database.commit()
    database.refresh(inventory_item)

    return inventory_item


def get_inventory_item(
    database: Session,
    inventory_id: int,
) -> Optional[InventoryItem]:
    """Return one inventory item by its database ID."""

    return database.get(InventoryItem, inventory_id)


def get_inventory_item_by_sku(
    database: Session,
    sku: str,
) -> Optional[InventoryItem]:
    """Return one inventory item by SKU."""

    statement = select(InventoryItem).where(
        InventoryItem.sku == sku
    )

    return database.scalar(statement)


def list_inventory_items(
    database: Session,
    skip: int = 0,
    limit: int = 100,
) -> List[InventoryItem]:
    """Return a paginated list of inventory items."""

    statement = (
        select(InventoryItem)
        .order_by(InventoryItem.id)
        .offset(skip)
        .limit(limit)
    )

    return list(database.scalars(statement).all())


def list_low_stock_items(
    database: Session,
    skip: int = 0,
    limit: int = 100,
) -> List[InventoryItem]:
    """Return inventory items at or below their reorder point."""

    statement = (
        select(InventoryItem)
        .where(
            InventoryItem.quantity
            <= InventoryItem.reorder_point
        )
        .order_by(
            InventoryItem.quantity,
            InventoryItem.id,
        )
        .offset(skip)
        .limit(limit)
    )

    return list(database.scalars(statement).all())


def update_inventory_item(
    database: Session,
    inventory_id: int,
    inventory_data: InventoryUpdate,
) -> Optional[InventoryItem]:
    """Update an existing inventory item."""

    inventory_item = get_inventory_item(
        database=database,
        inventory_id=inventory_id,
    )

    if inventory_item is None:
        return None

    update_data = inventory_data.model_dump(
        exclude_unset=True
    )

    new_sku = update_data.get("sku")

    if new_sku is not None and new_sku != inventory_item.sku:
        existing_item = get_inventory_item_by_sku(
            database=database,
            sku=new_sku,
        )

        if existing_item is not None:
            raise ValueError(
                f"An inventory item with SKU '{new_sku}' already exists."
            )

    for field_name, field_value in update_data.items():
        setattr(inventory_item, field_name, field_value)

    database.add(inventory_item)
    database.commit()
    database.refresh(inventory_item)

    return inventory_item


def delete_inventory_item(
    database: Session,
    inventory_id: int,
) -> bool:
    """Delete an inventory item and return whether it existed."""

    inventory_item = get_inventory_item(
        database=database,
        inventory_id=inventory_id,
    )

    if inventory_item is None:
        return False

    database.delete(inventory_item)
    database.commit()

    return True