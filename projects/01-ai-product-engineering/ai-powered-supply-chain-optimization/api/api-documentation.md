# API Documentation

## Document Purpose

This document defines the target API contract for the AI-Powered Supply Chain Optimization Platform.

It describes the intended service boundaries, endpoint structure, authentication model, request and response formats, validation rules, asynchronous workflows, error handling, observability requirements, and versioning policy.

An endpoint must only be described as implemented, tested, deployed, or production-ready after corresponding source code, automated test output, live API evidence, configuration, or deployment evidence has been added to this repository.

---

## API Design Principles

1. REST-oriented resource design
2. Versioned public interfaces
3. JSON request and response bodies
4. Explicit schema validation
5. Consistent error envelopes
6. Authentication and role-based authorization
7. Idempotency for sensitive write operations
8. Asynchronous execution for long-running AI workloads
9. Pagination for collection endpoints
10. Correlation IDs for traceability
11. Auditable business operations
12. Backward-compatible evolution where possible

---

## Base URL

```text
Development:
http://localhost:8000/api/v1

Production:
https://<production-domain>/api/v1
```

---

## Interactive Documentation

When enabled by the deployed FastAPI application:

```text
Swagger UI:
https://<production-domain>/docs

OpenAPI Schema:
https://<production-domain>/openapi.json

ReDoc:
https://<production-domain>/redoc
```

Production exposure of interactive documentation must follow the deployment security policy.

---

## Content Type

All request and response payloads use:

```http
Content-Type: application/json
Accept: application/json
```

File-import endpoints may additionally accept:

```http
Content-Type: multipart/form-data
```

---

## Authentication

Protected endpoints require a bearer access token:

```http
Authorization: Bearer <access_token>
```

The authentication layer is responsible for:

- User identity verification
- Token validation
- Token expiration enforcement
- Role resolution
- Permission checks
- Audit-event generation

---

## Authorization Roles

| Role | Primary Access |
|---|---|
| `admin` | Platform administration, configuration, users, audit access |
| `supply_chain_manager` | Forecasts, inventory, logistics, recommendations |
| `inventory_planner` | Inventory, reorder points, safety stock, forecasts |
| `procurement_manager` | Suppliers, procurement recommendations, supplier risk |
| `logistics_manager` | Shipment planning and logistics optimization |
| `analyst` | Read-only analytics, forecasts, reports, model outputs |
| `service_account` | Controlled machine-to-machine integration |

Every protected operation must apply least-privilege authorization.

---

## Standard Request Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
Accept: application/json
X-Correlation-ID: <uuid>
Idempotency-Key: <uuid>
```

### Header Rules

- `X-Correlation-ID` should be returned in the response.
- The server may generate a correlation ID when none is supplied.
- `Idempotency-Key` is required for selected write operations.
- Authentication tokens must never be included in URLs or logs.

---

## Standard Success Response

```json
{
  "success": true,
  "data": {},
  "meta": {
    "request_id": "c4ab961d-4f58-45c8-838f-62d9e71a4c02",
    "timestamp": "2026-07-12T12:00:00Z",
    "api_version": "v1"
  }
}
```

---

## Standard Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request payload is invalid.",
    "details": [
      {
        "field": "forecast_horizon_days",
        "message": "Value must be between 1 and 365."
      }
    ]
  },
  "meta": {
    "request_id": "c4ab961d-4f58-45c8-838f-62d9e71a4c02",
    "timestamp": "2026-07-12T12:00:00Z",
    "api_version": "v1"
  }
}
```

---

## HTTP Status Codes

| Status | Meaning |
|---:|---|
| `200` | Request completed successfully |
| `201` | Resource created successfully |
| `202` | Asynchronous task accepted |
| `204` | Request succeeded with no response body |
| `400` | Invalid request |
| `401` | Authentication required or invalid |
| `403` | Authenticated but not authorized |
| `404` | Resource not found |
| `409` | Resource or state conflict |
| `422` | Schema or semantic validation failure |
| `429` | Rate limit exceeded |
| `500` | Internal server error |
| `502` | Upstream dependency failure |
| `503` | Service temporarily unavailable |
| `504` | Upstream or task timeout |

---

## Health and Readiness

### Health Check

```http
GET /health
```

#### Example Response

```json
{
  "status": "healthy",
  "service": "supply-chain-api",
  "version": "1.0.0",
  "timestamp": "2026-07-12T12:00:00Z"
}
```

### Readiness Check

```http
GET /ready
```

#### Example Response

```json
{
  "status": "ready",
  "dependencies": {
    "database": "available",
    "cache": "available",
    "task_queue": "available",
    "model_registry": "available"
  }
}
```

Readiness must fail when a required production dependency is unavailable.

---

# Authentication API

## Sign In

```http
POST /auth/login
```

### Request

```json
{
  "email": "user@example.com",
  "password": "<password>"
}
```

### Response

```json
{
  "success": true,
  "data": {
    "access_token": "<access_token>",
    "refresh_token": "<refresh_token>",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

---

## Refresh Access Token

```http
POST /auth/refresh
```

### Request

```json
{
  "refresh_token": "<refresh_token>"
}
```

---

## Current User

```http
GET /auth/me
```

### Response

```json
{
  "success": true,
  "data": {
    "id": "usr_01J2ABCDEF",
    "email": "user@example.com",
    "roles": [
      "supply_chain_manager"
    ],
    "active": true
  }
}
```

---

# Product API

## List Products

```http
GET /products
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `page` | integer | No | Page number |
| `page_size` | integer | No | Results per page |
| `search` | string | No | Search by SKU or product name |
| `active` | boolean | No | Filter by active status |
| `category` | string | No | Filter by category |

### Example Response

```json
{
  "success": true,
  "data": [
    {
      "id": "prd_01J2ABCDEF",
      "sku": "SKU-10001",
      "name": "Industrial Component",
      "category": "components",
      "active": true
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 25,
    "total_items": 1,
    "total_pages": 1
  }
}
```

---

## Get Product

```http
GET /products/{product_id}
```

---

## Create Product

```http
POST /products
```

### Request

```json
{
  "sku": "SKU-10001",
  "name": "Industrial Component",
  "category": "components",
  "unit_of_measure": "unit",
  "lead_time_days": 14,
  "active": true
}
```

---

## Update Product

```http
PATCH /products/{product_id}
```

---

# Supplier API

## List Suppliers

```http
GET /suppliers
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `page` | integer | No | Page number |
| `page_size` | integer | No | Results per page |
| `search` | string | No | Supplier-name search |
| `country` | string | No | Country filter |
| `risk_level` | string | No | `low`, `medium`, `high`, `critical` |
| `active` | boolean | No | Active status |

---

## Get Supplier

```http
GET /suppliers/{supplier_id}
```

---

## Create Supplier

```http
POST /suppliers
```

### Request

```json
{
  "name": "Example Supplier GmbH",
  "country": "Germany",
  "currency": "EUR",
  "average_lead_time_days": 12,
  "minimum_order_value": 5000,
  "active": true
}
```

---

## Update Supplier

```http
PATCH /suppliers/{supplier_id}
```

---

# Inventory API

## Inventory Snapshot

```http
GET /inventory
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `product_id` | string | No | Product filter |
| `location_id` | string | No | Warehouse or location filter |
| `below_reorder_point` | boolean | No | Low-stock filter |
| `page` | integer | No | Page number |
| `page_size` | integer | No | Results per page |

---

## Get Inventory Position

```http
GET /inventory/{inventory_id}
```

### Response

```json
{
  "success": true,
  "data": {
    "id": "inv_01J2ABCDEF",
    "product_id": "prd_01J2ABCDEF",
    "location_id": "loc_01J2ABCDEF",
    "quantity_on_hand": 1250,
    "quantity_reserved": 160,
    "quantity_available": 1090,
    "reorder_point": 900,
    "safety_stock": 250,
    "updated_at": "2026-07-12T12:00:00Z"
  }
}
```

---

## Adjust Inventory

```http
POST /inventory/{inventory_id}/adjustments
```

### Required Header

```http
Idempotency-Key: <uuid>
```

### Request

```json
{
  "adjustment_type": "cycle_count",
  "quantity_delta": -10,
  "reason": "Physical count correction",
  "reference": "COUNT-2026-001"
}
```

This operation must create an audit event and must not silently overwrite historical inventory movements.

---

# Demand Forecasting API

## Create Forecast Job

```http
POST /forecasts
```

### Request

```json
{
  "product_ids": [
    "prd_01J2ABCDEF"
  ],
  "location_ids": [
    "loc_01J2ABCDEF"
  ],
  "forecast_horizon_days": 90,
  "granularity": "daily",
  "model_version": "approved-default",
  "include_confidence_intervals": true
}
```

### Response

```json
{
  "success": true,
  "data": {
    "job_id": "job_01J2ABCDEF",
    "status": "queued",
    "submitted_at": "2026-07-12T12:00:00Z"
  },
  "meta": {
    "request_id": "c4ab961d-4f58-45c8-838f-62d9e71a4c02"
  }
}
```

Expected status:

```http
202 Accepted
```

---

## List Forecasts

```http
GET /forecasts
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `product_id` | string | No | Product filter |
| `location_id` | string | No | Location filter |
| `status` | string | No | Job or forecast status |
| `from_date` | date | No | Forecast start date |
| `to_date` | date | No | Forecast end date |
| `model_version` | string | No | Model-version filter |

---

## Get Forecast

```http
GET /forecasts/{forecast_id}
```

### Response

```json
{
  "success": true,
  "data": {
    "forecast_id": "fct_01J2ABCDEF",
    "product_id": "prd_01J2ABCDEF",
    "location_id": "loc_01J2ABCDEF",
    "model_version": "demand-forecast-v3.2.0",
    "granularity": "daily",
    "generated_at": "2026-07-12T12:00:00Z",
    "predictions": [
      {
        "date": "2026-07-13",
        "predicted_demand": 142.8,
        "lower_bound": 125.2,
        "upper_bound": 160.4
      }
    ]
  }
}
```

---

# Inventory Optimization API

## Create Optimization Job

```http
POST /inventory/optimizations
```

### Request

```json
{
  "product_ids": [
    "prd_01J2ABCDEF"
  ],
  "location_ids": [
    "loc_01J2ABCDEF"
  ],
  "service_level_target": 0.95,
  "planning_horizon_days": 90,
  "constraints": {
    "maximum_inventory_value": 500000,
    "warehouse_capacity_units": 20000
  }
}
```

### Response

```json
{
  "success": true,
  "data": {
    "job_id": "job_01J2OPTIMIZE",
    "status": "queued"
  }
}
```

---

## Get Optimization Result

```http
GET /inventory/optimizations/{optimization_id}
```

### Response

```json
{
  "success": true,
  "data": {
    "optimization_id": "opt_01J2ABCDEF",
    "product_id": "prd_01J2ABCDEF",
    "location_id": "loc_01J2ABCDEF",
    "recommended_reorder_point": 980,
    "recommended_safety_stock": 290,
    "recommended_order_quantity": 1400,
    "estimated_stockout_reduction_percent": 18.4,
    "estimated_inventory_cost_change_percent": -7.2,
    "assumptions": [
      "Lead-time distribution derived from approved historical data",
      "Target service level set to 95 percent"
    ]
  }
}
```

Any estimated outcome must be clearly distinguished from a measured production result.

---

# Supplier Risk API

## Create Supplier Risk Assessment

```http
POST /supplier-risk/assessments
```

### Request

```json
{
  "supplier_ids": [
    "sup_01J2ABCDEF"
  ],
  "assessment_window_days": 180,
  "include_external_signals": false
}
```

---

## Get Supplier Risk Assessment

```http
GET /supplier-risk/assessments/{assessment_id}
```

### Response

```json
{
  "success": true,
  "data": {
    "assessment_id": "rsa_01J2ABCDEF",
    "supplier_id": "sup_01J2ABCDEF",
    "risk_score": 0.63,
    "risk_level": "high",
    "model_version": "supplier-risk-v2.1.0",
    "factors": [
      {
        "name": "late_delivery_rate",
        "contribution": 0.31
      },
      {
        "name": "quality_incident_rate",
        "contribution": 0.22
      }
    ],
    "generated_at": "2026-07-12T12:00:00Z"
  }
}
```

Risk scores must include model version, evaluation timestamp, and explainability metadata.

---

# Logistics Optimization API

## Create Logistics Optimization Job

```http
POST /logistics/optimizations
```

### Request

```json
{
  "shipment_ids": [
    "shp_01J2ABCDEF"
  ],
  "objective": "balanced",
  "constraints": {
    "maximum_delivery_days": 4,
    "maximum_total_cost": 15000,
    "capacity_required": 1200
  }
}
```

Supported objective values:

```text
minimum_cost
minimum_time
minimum_emissions
balanced
```

---

## Get Logistics Optimization Result

```http
GET /logistics/optimizations/{optimization_id}
```

---

# Procurement Recommendation API

## Generate Procurement Recommendations

```http
POST /procurement/recommendations
```

### Request

```json
{
  "product_ids": [
    "prd_01J2ABCDEF"
  ],
  "location_ids": [
    "loc_01J2ABCDEF"
  ],
  "planning_horizon_days": 60,
  "maximum_recommendations": 10
}
```

---

## Get Procurement Recommendation

```http
GET /procurement/recommendations/{recommendation_id}
```

### Response

```json
{
  "success": true,
  "data": {
    "recommendation_id": "rec_01J2ABCDEF",
    "product_id": "prd_01J2ABCDEF",
    "recommended_supplier_id": "sup_01J2ABCDEF",
    "recommended_quantity": 1500,
    "recommended_order_date": "2026-07-18",
    "estimated_cost": 47500,
    "confidence_score": 0.86,
    "reasoning": [
      "Forecasted demand exceeds current available inventory",
      "Supplier lead time satisfies planning constraints",
      "Supplier risk score is within the approved threshold"
    ],
    "approval_status": "pending"
  }
}
```

The recommendation endpoint must not automatically execute a purchase order unless a separate authorized workflow explicitly permits it.

---

# AI Explanation API

## Explain Forecast

```http
POST /ai/explanations/forecast
```

### Request

```json
{
  "forecast_id": "fct_01J2ABCDEF",
  "audience": "executive",
  "language": "en",
  "include_sources": true
}
```

### Response

```json
{
  "success": true,
  "data": {
    "summary": "Demand is expected to increase during the next planning period.",
    "key_drivers": [
      "Recent sales growth",
      "Seasonal demand pattern",
      "Reduced available inventory"
    ],
    "source_references": [
      {
        "type": "forecast",
        "id": "fct_01J2ABCDEF"
      }
    ],
    "generated_by": {
      "provider": "approved-provider",
      "model": "approved-model",
      "prompt_version": "forecast-explanation-v1"
    }
  }
}
```

The AI explanation layer must:

- Use approved data only
- Preserve source references
- Avoid fabricating operational facts
- Clearly distinguish explanation from authoritative transactional data
- Apply access-control filtering before retrieval

---

# Background Job API

## Get Job Status

```http
GET /jobs/{job_id}
```

### Response

```json
{
  "success": true,
  "data": {
    "job_id": "job_01J2ABCDEF",
    "job_type": "demand_forecast",
    "status": "running",
    "progress_percent": 65,
    "created_at": "2026-07-12T12:00:00Z",
    "started_at": "2026-07-12T12:00:04Z",
    "completed_at": null,
    "result_reference": null
  }
}
```

Supported job states:

```text
queued
running
completed
failed
cancelled
expired
```

---

## Cancel Job

```http
POST /jobs/{job_id}/cancel
```

Cancellation must be permitted only when the task state and authorization policy allow it.

---

# Data Import API

## Create Import Job

```http
POST /imports
```

### Multipart Fields

| Field | Required | Description |
|---|---:|---|
| `file` | Yes | Approved CSV or JSON file |
| `data_type` | Yes | Product, supplier, order, inventory, or shipment |
| `validate_only` | No | Validate without persisting records |
| `source_system` | Yes | Originating system identifier |

### Import Controls

- File-size limit
- File-type allowlist
- Malware scanning
- Schema validation
- Duplicate detection
- Row-level error reporting
- Atomic or controlled partial processing
- Audit-event creation

---

## Get Import Result

```http
GET /imports/{import_id}
```

### Response

```json
{
  "success": true,
  "data": {
    "import_id": "imp_01J2ABCDEF",
    "status": "completed",
    "total_rows": 1000,
    "accepted_rows": 982,
    "rejected_rows": 18,
    "error_report_url": "/imports/imp_01J2ABCDEF/errors"
  }
}
```

---

# Model Registry API

## List Approved Models

```http
GET /models
```

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `model_type` | string | No | Forecasting, risk, optimization, or explanation |
| `status` | string | No | Candidate, approved, deployed, retired |
| `environment` | string | No | Development, staging, production |

---

## Get Model Metadata

```http
GET /models/{model_id}
```

### Response

```json
{
  "success": true,
  "data": {
    "model_id": "mdl_01J2ABCDEF",
    "name": "demand-forecast",
    "version": "3.2.0",
    "status": "approved",
    "environment": "production",
    "evaluation_metrics": {
      "mae": 8.42,
      "rmse": 11.37,
      "mape_percent": 7.91
    },
    "approved_at": "2026-07-10T09:00:00Z",
    "approved_by": "usr_01J2APPROVER"
  }
}
```

Metric values must only be published when supported by reproducible evaluation evidence.

---

# Audit API

## List Audit Events

```http
GET /audit-events
```

Access should normally be restricted to administrative or compliance roles.

### Query Parameters

| Parameter | Type | Required | Description |
|---|---|---:|---|
| `actor_id` | string | No | Filter by user or service account |
| `action` | string | No | Filter by operation |
| `resource_type` | string | No | Filter by resource |
| `from_timestamp` | datetime | No | Start of time range |
| `to_timestamp` | datetime | No | End of time range |

Audit records must be immutable through the public application API.

---

# Pagination

Collection endpoints use page-based pagination unless cursor pagination is required for scale.

### Request

```http
GET /products?page=1&page_size=25
```

### Response Metadata

```json
{
  "page": 1,
  "page_size": 25,
  "total_items": 240,
  "total_pages": 10
}
```

Maximum page size must be enforced by the API.

---

# Filtering and Sorting

Example:

```http
GET /suppliers?risk_level=high&country=Germany&sort=-risk_score
```

Sorting fields must be explicitly allowlisted to prevent unsafe dynamic queries.

---

# Validation Rules

The API must validate:

- Required fields
- Identifier formats
- Enum values
- Date ranges
- Numeric limits
- Referential integrity
- Duplicate operations
- Business-state transitions
- User permissions
- File constraints
- Model approval status
- Planning constraints

Validation must occur before side effects are committed.

---

# Idempotency

Idempotency is required for operations such as:

- Inventory adjustments
- Import creation
- Purchase-order creation
- External integration callbacks
- Sensitive workflow transitions

The same idempotency key and equivalent request payload should return the original result rather than create a duplicate operation.

---

# Rate Limiting

Rate limits should be applied by:

- Authenticated identity
- Service account
- API key
- IP address where appropriate
- Endpoint cost category

### Example Response

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "The request limit has been exceeded."
  }
}
```

---

# API Versioning

The initial contract uses:

```text
/api/v1
```

Breaking changes require a new major API version.

Non-breaking changes may include:

- Optional response fields
- Optional request fields
- New endpoints
- New enum values only when clients are designed to tolerate them
- Additional metadata

Deprecated endpoints must include a migration period and documented replacement.

---

# Observability Requirements

Every request should produce:

- Correlation ID
- Request duration
- Route identifier
- HTTP method
- Response status
- Authenticated actor reference
- Structured error code when applicable
- Trace context
- Dependency timing
- Audit event for sensitive operations

Logs must not include:

- Plain-text passwords
- Access tokens
- Refresh tokens
- Secret keys
- Sensitive personal data
- Unapproved operational payloads

---

# Security Requirements

- HTTPS is mandatory in production.
- Authentication is required for protected endpoints.
- Authorization must be checked server-side.
- Secrets must remain outside source control.
- Input and output schemas must be validated.
- Database access must use parameterized operations.
- CORS origins must be explicitly configured.
- File uploads must be scanned and restricted.
- External AI calls must follow approved data controls.
- Administrative endpoints must use stronger access restrictions.
- Security-relevant events must be auditable.
- Production debug information must not be exposed to clients.

---

# API Testing Requirements

The API test suite should cover:

- Authentication success and failure
- Authorization boundaries
- Request validation
- Response-schema validation
- Pagination
- Filtering and sorting
- Idempotency
- Rate limiting
- Async job lifecycle
- Dependency failure
- Timeout behavior
- Database transaction rollback
- Model-version validation
- Audit-event generation
- Sensitive-data handling
- Backward compatibility

---

# Contract Validation Checklist

- [ ] OpenAPI schema generated successfully
- [ ] Every endpoint has an explicit request schema
- [ ] Every endpoint has an explicit response schema
- [ ] Authentication requirements are documented
- [ ] Authorization rules are documented
- [ ] Error responses use the standard envelope
- [ ] Pagination limits are enforced
- [ ] Idempotency is tested where required
- [ ] Long-running workloads return `202 Accepted`
- [ ] Correlation IDs are propagated
- [ ] Sensitive values are excluded from logs
- [ ] Model versions are returned with AI outputs
- [ ] Estimated outcomes are not presented as measured results
- [ ] Implemented endpoints have corresponding test evidence
- [ ] Deployed endpoints have corresponding live-system evidence

---

## Current Evidence Status

This document defines the target API contract.

Endpoints, metrics, model versions, performance claims, and deployment URLs shown here are architectural examples unless corresponding implementation evidence has been added to the repository.

A capability must only be marked as implemented, tested, deployed, live, or production-ready when it is supported by verifiable source code, test output, configuration, deployment evidence, or a functioning live endpoint.