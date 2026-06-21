# Contratos API MVP

## Objetivo

Definir los endpoints iniciales de ProvCore para implementar el MVP backend-first con FastAPI.

El documento baja el dominio a contratos funcionales suficientemente concretos para empezar a desarrollar sin perder arquitectura.

## Principios

- La API expone casos de uso, no CRUD libre de tablas.
- Los routers llaman a application.
- Los routers no contienen reglas de negocio.
- El dominio no conoce HTTP.
- Todo endpoint protegido valida usuario, rol, permiso y alcance.
- Toda operación fiscal, contable o de provisión requiere `tenant_id` y `legal_entity_id`.
- Toda decisión relevante genera auditoría.

## Convenciones generales

### Prefijo

```text
/api/v1
```

### Cabeceras conceptuales

En MVP se podrán simular, pero el contrato debe prever:

```text
Authorization: Bearer <token>
X-Correlation-Id: corr_123
X-Tenant-Id: tenant_001
X-Legal-Entity-Id: le_001
```

Regla:

```text
El backend valida el contexto. No confía ciegamente en la cabecera.
```

### Formato de respuesta

Respuesta de comando:

```json
{
  "data": {},
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_123"
  }
}
```

Respuesta de consulta:

```json
{
  "data": [],
  "meta": {
    "correlation_id": "corr_123",
    "pagination": {
      "limit": 50,
      "offset": 0,
      "total": 0
    }
  }
}
```

### Formato de error

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Mensaje funcional legible.",
    "details": {},
    "correlation_id": "corr_123"
  }
}
```

## Módulos API iniciales

```text
/api/v1/internal-orders
/api/v1/provisions
/api/v1/invoices
/api/v1/suppliers
/api/v1/audit-events
/api/v1/analytics
/api/v1/alerts
```

## Endpoints P0

### Crear pedido interno

```text
POST /api/v1/internal-orders
```

Caso de uso:

```text
CreateInternalOrder
```

Actor:

- usuario operativo.

Permiso:

```text
create_internal_order
```

Contexto:

- `tenant_id`.
- `legal_entity_id`.
- `user_id`.
- `correlation_id`.

Request:

```json
{
  "area": "operaciones",
  "cost_center": "CC-001",
  "operational_supplier_name": "Proveedor conocido",
  "description": "Servicio mensual",
  "expense_type": "servicio",
  "service_type": "recurrente",
  "estimated_amount": {
    "amount": "1200.00",
    "currency": "EUR"
  },
  "service_period": {
    "from": "2026-07-01",
    "to": "2026-07-31"
  },
  "expected_invoice_date": "2026-08-05",
  "expects_invoice": true,
  "is_recurring": false
}
```

Response `201 Created`:

```json
{
  "data": {
    "internal_order_id": "io_001",
    "status": "Enviado",
    "provision_id": null
  },
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_001"
  }
}
```

Auditoría:

- pedido interno creado.

Errores:

- `LEGAL_ENTITY_NOT_ALLOWED`.
- `INVALID_AMOUNT`.
- `MISSING_REQUIRED_FIELD`.
- `FORBIDDEN_OPERATION`.

### Enviar pedido y generar provisión

```text
POST /api/v1/internal-orders/{internal_order_id}/submit
```

Caso de uso:

```text
GenerateProvisionFromMovement
```

Actor:

- usuario operativo.

Permiso:

```text
submit_internal_order
```

Request:

```json
{
  "comment": "Compromiso confirmado por el responsable."
}
```

Response `200 OK`:

```json
{
  "data": {
    "internal_order_id": "io_001",
    "internal_order_status": "ProvisionGenerada",
    "provision_id": "prov_001",
    "provision_status": "PendienteValidacionFinanciera",
    "requires_supplier_mapping": true
  },
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_002"
  }
}
```

Auditoría:

- pedido enviado.
- provisión creada.
- movimiento provisionable identificado.

Eventos:

- `PROVISIONABLE_MOVEMENT_IDENTIFIED`.
- `PROVISION_CREATED`.

Errores:

- `INTERNAL_ORDER_NOT_FOUND`.
- `INTERNAL_ORDER_NOT_SUBMITTABLE`.
- `LEGAL_ENTITY_NOT_ALLOWED`.
- `SUPPLIER_MAPPING_REQUIRED`.

### Consultar provisión

```text
GET /api/v1/provisions/{provision_id}
```

Caso de uso:

```text
GetProvisionDetail
```

Actor:

- usuario operativo si está dentro de su ámbito.
- usuario financiero autorizado.

Permiso:

```text
view_provision
```

Response `200 OK`:

```json
{
  "data": {
    "provision_id": "prov_001",
    "origin_type": "PedidoInternoProveedor",
    "origin_id": "io_001",
    "status": "Abierta",
    "operational_supplier_name": "Proveedor conocido",
    "fiscal_supplier_id": "fs_001",
    "amounts": {
      "provisioned": "1200.00",
      "consumed": "0.00",
      "pending": "1200.00",
      "currency": "EUR"
    },
    "service_period": {
      "from": "2026-07-01",
      "to": "2026-07-31"
    }
  },
  "meta": {
    "correlation_id": "corr_123"
  }
}
```

Errores:

- `PROVISION_NOT_FOUND`.
- `FORBIDDEN_SCOPE`.

### Registrar factura

```text
POST /api/v1/invoices
```

Caso de uso:

```text
RegisterInvoice
```

Actor:

- usuario financiero autorizado.
- servicio de integración si la entrada viene de OCR o buzón.

Permiso:

```text
register_invoice
```

Request:

```json
{
  "invoice_number": "F-2026-001",
  "invoice_date": "2026-08-01",
  "received_date": "2026-08-02",
  "detected_supplier": {
    "name": "Proveedor Fiscal S.L.",
    "tax_id": "B00000000",
    "country": "ES"
  },
  "amounts": {
    "tax_base": "1000.00",
    "tax_amount": "210.00",
    "total": "1210.00",
    "currency": "EUR"
  },
  "document_source": "manual_upload"
}
```

Response `201 Created`:

```json
{
  "data": {
    "invoice_id": "inv_001",
    "status": "ProveedorDetectado",
    "fiscal_supplier_id": null,
    "requires_supplier_onboarding": true
  },
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_003"
  }
}
```

Auditoría:

- factura registrada.
- proveedor fiscal detectado.

Eventos:

- `INVOICE_REGISTERED`.
- `FISCAL_SUPPLIER_DETECTED`.

Errores:

- `DUPLICATED_INVOICE`.
- `INVALID_TAX_AMOUNT`.
- `LEGAL_ENTITY_NOT_ALLOWED`.
- `SUPPLIER_ONBOARDING_REQUIRED`.

### Buscar provisiones compatibles

```text
GET /api/v1/invoices/{invoice_id}/compatible-provisions
```

Caso de uso:

```text
FindCompatibleProvisions
```

Actor:

- usuario financiero autorizado.

Permiso:

```text
find_compatible_provisions
```

Query params:

```text
min_score=0.70
limit=20
```

Response `200 OK`:

```json
{
  "data": [
    {
      "provision_id": "prov_001",
      "status": "Abierta",
      "pending_amount": "1200.00",
      "currency": "EUR",
      "score": "0.92",
      "reasons": [
        "same_legal_entity",
        "same_supplier",
        "amount_close",
        "period_overlap"
      ]
    }
  ],
  "meta": {
    "correlation_id": "corr_123"
  }
}
```

Eventos:

- `MATCHING_SUGGESTED`.

Errores:

- `INVOICE_NOT_FOUND`.
- `INVOICE_BLOCKED`.
- `FISCAL_SUPPLIER_NOT_VALIDATED`.

### Aprobar consumo factura-provisión

```text
POST /api/v1/invoices/{invoice_id}/provision-consumptions
```

Caso de uso:

```text
ApproveProvisionConsumption
```

Actor:

- usuario financiero autorizado.

Permiso:

```text
approve_provision_consumption
```

Request:

```json
{
  "items": [
    {
      "provision_id": "prov_001",
      "amount": "1000.00",
      "currency": "EUR",
      "reason": "Factura correspondiente al servicio provisionado."
    }
  ],
  "approval_comment": "Consumo revisado y aprobado."
}
```

Response `200 OK`:

```json
{
  "data": {
    "invoice_id": "inv_001",
    "invoice_status": "PendienteRevisionContable",
    "consumptions": [
      {
        "consumption_id": "cons_001",
        "provision_id": "prov_001",
        "status": "Aprobada",
        "amount": "1000.00",
        "currency": "EUR",
        "difference_amount": "200.00",
        "requires_regularization": true
      }
    ]
  },
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_004"
  }
}
```

Auditoría:

- consumo aprobado.
- importe de provisión actualizado.
- diferencia detectada si aplica.

Eventos:

- `PROVISION_CONSUMPTION_APPROVED`.
- `REGULARIZATION_REQUIRED` si aplica.

Errores:

- `INVOICE_NOT_FOUND`.
- `PROVISION_NOT_FOUND`.
- `PROVISION_NOT_CONSUMABLE`.
- `CONSUMPTION_AMOUNT_EXCEEDS_PENDING`.
- `CURRENCY_MISMATCH`.
- `FORBIDDEN_OPERATION`.

### Crear provisión tardía auditada

```text
POST /api/v1/invoices/{invoice_id}/late-provision
```

Caso de uso:

```text
CreateLateProvision
```

Actor:

- usuario financiero autorizado.

Permiso:

```text
create_late_provision
```

Request:

```json
{
  "reason": "Factura recibida sin pedido interno previo.",
  "responsible_user_id": "usr_010",
  "amount": {
    "amount": "1210.00",
    "currency": "EUR"
  },
  "comment": "Excepción aprobada para no bloquear el registro."
}
```

Response `201 Created`:

```json
{
  "data": {
    "invoice_id": "inv_001",
    "provision_id": "prov_late_001",
    "provision_status": "ConsumidaTotalmente",
    "invoice_status": "PendienteRevisionContable",
    "is_late_provision": true
  },
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_005"
  }
}
```

Auditoría:

- provisión tardía creada.
- motivo registrado.
- consumo inmediato registrado.

Eventos:

- `LATE_PROVISION_CREATED`.
- `PROVISION_CONSUMPTION_APPROVED`.

Errores:

- `INVOICE_NOT_FOUND`.
- `INVOICE_ALREADY_HAS_APPROVED_CONSUMPTION`.
- `LATE_PROVISION_REASON_REQUIRED`.
- `FISCAL_SUPPLIER_NOT_VALIDATED`.

### Consultar auditoría de una entidad

```text
GET /api/v1/audit-events
```

Caso de uso:

```text
SearchAuditEvents
```

Actor:

- usuario financiero autorizado.
- auditor.

Permiso:

```text
view_audit_log
```

Query params:

```text
entity_type=provision
entity_id=prov_001
limit=50
offset=0
```

Response `200 OK`:

```json
{
  "data": [
    {
      "audit_event_id": "aud_004",
      "entity_type": "provision",
      "entity_id": "prov_001",
      "action": "PROVISION_CONSUMPTION_APPROVED",
      "previous_status": "Abierta",
      "new_status": "ConsumidaParcialmente",
      "user_id": "usr_002",
      "role_used": "UsuarioFinancieroAutorizado",
      "permission_used": "approve_provision_consumption",
      "reason": "Consumo revisado y aprobado.",
      "created_at": "2026-08-02T10:30:00Z"
    }
  ],
  "meta": {
    "correlation_id": "corr_123",
    "pagination": {
      "limit": 50,
      "offset": 0,
      "total": 1
    }
  }
}
```

Errores:

- `FORBIDDEN_SCOPE`.
- `INVALID_ENTITY_TYPE`.

## Endpoints P1

### Validar mapeo proveedor

```text
POST /api/v1/supplier-mappings/{supplier_mapping_id}/validate
```

Caso de uso:

```text
ValidateSupplierMapping
```

Actor:

- usuario financiero autorizado.

Permiso:

```text
approve_supplier_mapping
```

Request:

```json
{
  "fiscal_supplier_id": "fs_001",
  "comment": "Proveedor fiscal validado para esta sociedad."
}
```

Response `200 OK`:

```json
{
  "data": {
    "supplier_mapping_id": "map_001",
    "status": "ValidadoFinanciero",
    "fiscal_supplier_id": "fs_001"
  },
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_006"
  }
}
```

### Crear solicitud de alta de proveedor fiscal

```text
POST /api/v1/invoices/{invoice_id}/supplier-onboarding-requests
```

Caso de uso:

```text
CreateSupplierOnboardingRequest
```

Actor:

- usuario financiero autorizado.

Permiso:

```text
validate_fiscal_supplier
```

Request:

```json
{
  "detected_supplier": {
    "name": "Proveedor Fiscal S.L.",
    "tax_id": "B00000000",
    "country": "ES",
    "address": "Calle Ejemplo 1"
  },
  "reason": "Proveedor no existente para la legal entity."
}
```

Response `201 Created`:

```json
{
  "data": {
    "supplier_onboarding_request_id": "sup_onb_001",
    "invoice_id": "inv_001",
    "status": "PendienteValidacionFinanciera"
  },
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_007"
  }
}
```

### Confirmar alta ERP simulada

```text
POST /api/v1/supplier-onboarding-requests/{request_id}/confirm-erp
```

Caso de uso:

```text
ConfirmSupplierCreatedInErp
```

Actor:

- servicio de integración.
- administrador técnico en modo simulado.

Permiso:

```text
submit_supplier_onboarding_to_erp
```

Request:

```json
{
  "erp_supplier_id": "ERP-SUP-001",
  "response_code": "200",
  "message": "Proveedor creado correctamente."
}
```

Response `200 OK`:

```json
{
  "data": {
    "supplier_onboarding_request_id": "sup_onb_001",
    "status": "ConfirmadaERP",
    "fiscal_supplier_id": "fs_001",
    "invoice_status": "PendienteProvision"
  },
  "meta": {
    "correlation_id": "corr_123",
    "audit_event_id": "aud_008"
  }
}
```

### Consultar analítica mínima

```text
GET /api/v1/analytics/provisions-summary
```

Caso de uso:

```text
GetProvisionAnalyticsSummary
```

Actor:

- usuario operativo dentro de su ámbito.
- usuario financiero autorizado.

Permiso:

```text
view_financial_analytics
```

Query params:

```text
period=2026-08
legal_entity_id=le_001
buyer_group_id=bg_001
```

Response `200 OK`:

```json
{
  "data": {
    "period": "2026-08",
    "provisioned_amount": "50000.00",
    "consumed_amount": "32000.00",
    "pending_amount": "18000.00",
    "late_provisions_count": 4,
    "blocked_invoices_count": 2,
    "currency": "EUR"
  },
  "meta": {
    "correlation_id": "corr_123"
  }
}
```

### Generar alertas de cierre

```text
POST /api/v1/closing-periods/{closing_period_id}/alerts/generate
```

Caso de uso:

```text
GenerateClosingAlerts
```

Actor:

- usuario financiero autorizado.

Permiso:

```text
resolve_closing_alert
```

Request:

```json
{
  "alert_types": [
    "open_provisions",
    "blocked_invoices",
    "pending_supplier_onboarding"
  ]
}
```

Response `202 Accepted`:

```json
{
  "data": {
    "closing_period_id": "cp_001",
    "generated_alerts": 12,
    "status": "accepted"
  },
  "meta": {
    "correlation_id": "corr_123"
  }
}
```

## Errores comunes

| Código | HTTP | Descripción |
| --- | --- | --- |
| `AUTHENTICATION_REQUIRED` | 401 | La petición no tiene usuario autenticado. |
| `FORBIDDEN_OPERATION` | 403 | El usuario no tiene el permiso requerido. |
| `FORBIDDEN_SCOPE` | 403 | El usuario no tiene acceso al tenant, legal entity o ámbito solicitado. |
| `LEGAL_ENTITY_REQUIRED` | 400 | La operación requiere legal entity. |
| `INVALID_STATE_TRANSITION` | 409 | La entidad no puede pasar al estado solicitado. |
| `RESOURCE_NOT_FOUND` | 404 | El recurso no existe dentro del alcance permitido. |
| `VALIDATION_ERROR` | 422 | Los datos no cumplen una regla de validación. |
| `DOMAIN_RULE_VIOLATION` | 422 | La operación incumple una regla de negocio. |

## Reglas de implementación futura

- Cada endpoint se implementará en `interface`.
- Cada endpoint llamará a un caso de uso de `application`.
- Cada caso de uso abrirá Unit of Work si modifica estado.
- Los repositorios concretos vivirán en `infrastructure`.
- Los errores de dominio se traducirán a HTTP en `interface`.
- Los permisos se resolverán antes de ejecutar el caso de uso.
- La auditoría se registrará dentro de la misma transacción cuando aplique.

## Primer orden de implementación recomendado

1. `POST /api/v1/internal-orders`.
2. `POST /api/v1/internal-orders/{internal_order_id}/submit`.
3. `POST /api/v1/invoices`.
4. `GET /api/v1/invoices/{invoice_id}/compatible-provisions`.
5. `POST /api/v1/invoices/{invoice_id}/provision-consumptions`.
6. `GET /api/v1/audit-events`.
7. `POST /api/v1/invoices/{invoice_id}/late-provision`.
