from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class InventoryBase(BaseModel):
    sku: str = Field(
        ...,
        min_length=1,
        max_length=64,
        description="Unique stock-keeping unit",
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Inventory item name",
    )
    quantity: int = Field(
        default=0,
        ge=0,
        description="Current available quantity",
    )
    reorder_point: int = Field(
        default=0,
        ge=0,
        description="Quantity threshold for replenishment",
    )
    unit_cost: Decimal = Field(
        default=Decimal("0.00"),
        ge=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        description="Cost per inventory unit",
    )
    lead_time_days: int = Field(
        default=0,
        ge=0,
        description="Supplier lead time in days",
    )


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    sku: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=64,
    )
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    quantity: Optional[int] = Field(
        default=None,
        ge=0,
    )
    reorder_point: Optional[int] = Field(
        default=None,
        ge=0,
    )
    unit_cost: Optional[Decimal] = Field(
        default=None,
        ge=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
    )
    lead_time_days: Optional[int] = Field(
        default=None,
        ge=0,
    )


class InventoryResponse(InventoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime