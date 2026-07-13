from collections.abc import Generator
from decimal import Decimal
from typing import Any, Optional

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app


API_PREFIX = "/api/v1"
INVENTORY_API = f"{API_PREFIX}/inventory"


def inventory_payload(
    *,
    sku: str = "SKU-001",
    name: str = "Test Inventory Item",
    quantity: int = 10,
    reorder_point: int = 5,
    unit_cost: str = "12.50",
    lead_time_days: int = 7,
) -> dict[str, Any]:
    return {
        "sku": sku,
        "name": name,
        "quantity": quantity,
        "reorder_point": reorder_point,
        "unit_cost": unit_cost,
        "lead_time_days": lead_time_days,
    }


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    test_engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    testing_session_local = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator[Session, None, None]:
        database = testing_session_local()

        try:
            yield database
        finally:
            database.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        test_client.close()
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


def create_item(
    client: TestClient,
    **overrides: Any,
) -> dict[str, Any]:
    payload = inventory_payload(**overrides)
    response = client.post(INVENTORY_API, json=payload)

    assert response.status_code == 201, response.text

    return response.json()


def test_system_endpoints(client: TestClient) -> None:
    root_response = client.get("/")
    assert root_response.status_code == 200

    root_body = root_response.json()
    assert root_body["status"] == "operational"
    assert root_body["documentation"] == "/docs"
    assert root_body["health_check"] == "/health"
    assert root_body["inventory_api"] == INVENTORY_API

    health_response = client.get("/health")
    assert health_response.status_code == 200

    health_body = health_response.json()
    assert health_body["status"] == "healthy"
    assert health_body["service"]
    assert health_body["version"]


def test_create_and_read_inventory_item(
    client: TestClient,
) -> None:
    created = create_item(client)

    assert created["id"] > 0
    assert created["sku"] == "SKU-001"
    assert created["name"] == "Test Inventory Item"
    assert created["quantity"] == 10
    assert created["reorder_point"] == 5
    assert Decimal(str(created["unit_cost"])) == Decimal("12.50")
    assert created["lead_time_days"] == 7
    assert created["created_at"]
    assert created["updated_at"]

    by_id_response = client.get(
        f"{INVENTORY_API}/{created['id']}"
    )
    assert by_id_response.status_code == 200
    assert by_id_response.json()["sku"] == "SKU-001"

    by_sku_response = client.get(
        f"{INVENTORY_API}/sku/SKU-001"
    )
    assert by_sku_response.status_code == 200
    assert by_sku_response.json()["id"] == created["id"]


def test_listing_pagination_and_low_stock(
    client: TestClient,
) -> None:
    create_item(
        client,
        sku="LOW-001",
        quantity=2,
        reorder_point=5,
    )
    create_item(
        client,
        sku="BOUNDARY-001",
        quantity=5,
        reorder_point=5,
    )
    create_item(
        client,
        sku="HEALTHY-001",
        quantity=10,
        reorder_point=5,
    )

    list_response = client.get(INVENTORY_API)
    assert list_response.status_code == 200
    assert len(list_response.json()) == 3

    page_response = client.get(
        INVENTORY_API,
        params={"skip": 1, "limit": 1},
    )
    assert page_response.status_code == 200
    assert len(page_response.json()) == 1
    assert page_response.json()[0]["sku"] == "BOUNDARY-001"

    low_stock_response = client.get(
        f"{INVENTORY_API}/low-stock"
    )
    assert low_stock_response.status_code == 200

    low_stock_skus = [
        item["sku"]
        for item in low_stock_response.json()
    ]

    assert low_stock_skus == [
        "LOW-001",
        "BOUNDARY-001",
    ]


def test_update_and_duplicate_sku_conflicts(
    client: TestClient,
) -> None:
    first_item = create_item(
        client,
        sku="SKU-FIRST",
    )
    second_item = create_item(
        client,
        sku="SKU-SECOND",
    )

    duplicate_create_response = client.post(
        INVENTORY_API,
        json=inventory_payload(sku="SKU-FIRST"),
    )
    assert duplicate_create_response.status_code == 409

    update_response = client.patch(
        f"{INVENTORY_API}/{second_item['id']}",
        json={
            "name": "Updated Inventory Item",
            "quantity": 3,
            "unit_cost": "15.75",
        },
    )
    assert update_response.status_code == 200

    updated = update_response.json()
    assert updated["name"] == "Updated Inventory Item"
    assert updated["quantity"] == 3
    assert Decimal(str(updated["unit_cost"])) == Decimal("15.75")

    duplicate_update_response = client.patch(
        f"{INVENTORY_API}/{second_item['id']}",
        json={"sku": first_item["sku"]},
    )
    assert duplicate_update_response.status_code == 409


def test_delete_inventory_item(
    client: TestClient,
) -> None:
    created = create_item(
        client,
        sku="DELETE-001",
    )

    delete_response = client.delete(
        f"{INVENTORY_API}/{created['id']}"
    )
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    missing_response = client.get(
        f"{INVENTORY_API}/{created['id']}"
    )
    assert missing_response.status_code == 404


@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        ("sku", ""),
        ("name", ""),
        ("quantity", -1),
        ("reorder_point", -1),
        ("unit_cost", "-0.01"),
        ("lead_time_days", -1),
    ],
)
def test_create_validation_rejects_invalid_values(
    client: TestClient,
    field_name: str,
    invalid_value: Any,
) -> None:
    payload = inventory_payload()
    payload[field_name] = invalid_value

    response = client.post(
        INVENTORY_API,
        json=payload,
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    ("method", "path", "body"),
    [
        ("GET", f"{INVENTORY_API}/999999", None),
        ("GET", f"{INVENTORY_API}/sku/DOES-NOT-EXIST", None),
        (
            "PATCH",
            f"{INVENTORY_API}/999999",
            {"quantity": 1},
        ),
        ("DELETE", f"{INVENTORY_API}/999999", None),
    ],
)
def test_missing_inventory_items_return_404(
    client: TestClient,
    method: str,
    path: str,
    body: Optional[dict[str, Any]],
) -> None:
    request_options: dict[str, Any] = {}

    if body is not None:
        request_options["json"] = body

    response = client.request(
        method,
        path,
        **request_options,
    )

    assert response.status_code == 404
