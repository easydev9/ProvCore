# Modelo de dominio MVP

## Objetivo

Definir las entidades, abstracciones y metodos conceptuales del dominio MVP antes de disenar contratos API o escribir codigo.

El objetivo es evitar que la API nazca como CRUD de tablas. La API debe exponer casos de uso derivados del dominio.

## Principio central

ProvCore no identifica solo pedidos, facturas o tarjetas.

ProvCore identifica movimientos provisionables.

Un movimiento provisionable tiene un origen y aporta los datos necesarios para que el motor comun pueda decidir si genera una provision, si requiere validacion, si esta incompleto o si genera una excepcion.

## Capas de logica

La logica no debe vivir toda en el mismo sitio.

```text
Entidad de dominio
  reglas propias de un objeto

Servicio de dominio
  reglas que involucran varias entidades

Caso de uso de application
  orquesta el flujo completo
```

## Abstraccion principal

### ProvisionableMovement

Contrato comun para cualquier entrada capaz de generar una provision.

Responsabilidad:

- exponer origen.
- exponer datos normalizados minimos.
- permitir crear una solicitud de provision.
- encapsular diferencias propias de cada origen.

Metodos conceptuales:

- `get_origin_type()`.
- `get_origin_id()`.
- `get_tenant_id()`.
- `get_legal_entity_id()`.
- `get_responsible_id()`.
- `get_operational_supplier()`.
- `get_amount()`.
- `get_currency()`.
- `get_period()`.
- `get_expense_type()`.
- `to_provision_request()`.
- `has_required_data()`.

Implementaciones futuras:

- `InternalOrderMovement`.
- `CardMovement`.
- `LateInvoiceMovement`.
- `RecurringSubscriptionMovement`.

El motor no debe depender de detalles internos de cada implementacion.

## Value objects

### Money

Representa importe y moneda.

Metodos conceptuales:

- `is_positive()`.
- `same_currency_as(other)`.
- `subtract(other)`.

### ServicePeriod

Representa periodo de servicio.

Metodos conceptuales:

- `contains(date)`.
- `overlaps(other)`.
- `to_accounting_period()`.

### ProvisionRequest

Objeto normalizado que recibe el motor para crear una provision.

Metodos conceptuales:

- `validate_required_fields()`.
- `validate_amount()`.
- `validate_origin()`.

## Entidades principales

### Provision

Entidad central del motor.

Responsabilidad:

- representar la obligacion provisionada.
- controlar importes.
- controlar estado.
- permitir consumo.
- detectar necesidad de regularizacion.

Metodos conceptuales:

- `can_be_consumed()`.
- `consume(amount)`.
- `calculate_pending_amount()`.
- `is_fully_consumed()`.
- `is_partially_consumed()`.
- `requires_regularization(real_amount)`.
- `mark_pending_regularization(reason)`.
- `close()`.
- `cancel(reason)`.
- `can_transition_to(new_status)`.

No debe:

- llamar a SQL Server.
- conocer FastAPI.
- crear auditoria directamente en infraestructura.

### ProvisionConsumption

Relacion entre factura y provision.

Responsabilidad:

- representar importe consumido.
- reflejar diferencia contra provision.
- controlar aprobacion o rechazo.

Metodos conceptuales:

- `approve(user_id)`.
- `reject(user_id, reason)`.
- `calculate_difference()`.
- `requires_regularization()`.

### InternalOrder

Origen operativo inicial.

Responsabilidad:

- capturar compromiso de gasto.
- validar datos operativos.
- actuar como movimiento provisionable.

Metodos conceptuales:

- `submit()`.
- `cancel(reason)`.
- `to_provision_request()`.
- `has_required_data()`.

No debe:

- implementar reglas propias de provision.
- consumir facturas.

### Invoice

Documento fiscal recibido.

Responsabilidad:

- representar datos de factura.
- controlar estados propios.
- indicar si tiene proveedor fiscal valido.
- indicar si puede continuar el flujo.

Metodos conceptuales:

- `mark_ocr_processed()`.
- `assign_fiscal_supplier(supplier_id)`.
- `mark_without_compatible_provision()`.
- `block(reason)`.
- `unblock(reason)`.
- `validate_functionally(user_id)`.
- `mark_registered()`.

No debe:

- decidir por si misma reglas de consumo de provision.
- crear proveedor fiscal directamente sin pasar por caso de uso.

### FiscalSupplier

Proveedor validado fiscalmente para una legal entity.

Responsabilidad:

- representar datos fiscales necesarios.
- reflejar estado de validacion o alta ERP.

Metodos conceptuales:

- `mark_detected_from_invoice()`.
- `mark_pending_erp_creation()`.
- `mark_created_in_erp(external_id)`.
- `validate_by_administration(user_id)`.
- `reject(reason)`.

### SupplierOnboardingRequest

Solicitud de alta o validacion de proveedor fiscal.

Responsabilidad:

- gobernar el flujo previo a registrar factura cuando el proveedor no existe en ERP para una legal entity.

Metodos conceptuales:

- `submit_for_validation()`.
- `mark_ready_to_send()`.
- `mark_sent_to_erp()`.
- `mark_confirmed(response_code)`.
- `mark_failed(reason)`.
- `cancel(reason)`.

Regla:

```text
La factura queda bloqueada hasta que el proveedor fiscal exista o quede validado para la legal entity.
```

### OperationalSupplier

Proveedor como lo conoce el usuario operativo.

Responsabilidad:

- representar alias o nombre operativo.
- servir de entrada para mapeo fiscal.

Metodos conceptuales:

- `normalize_alias()`.
- `deactivate()`.

### SupplierMapping

Relacion entre proveedor operativo y proveedor fiscal.

Responsabilidad:

- guardar sugerencia.
- guardar validacion.
- permitir correccion.

Metodos conceptuales:

- `suggest(candidate, confidence)`.
- `validate_by_administration(user_id)`.
- `reject(user_id, reason)`.
- `correct(new_supplier_id, reason)`.

### MatchingSuggestion

Sugerencia generada por regla, historico o IA.

Responsabilidad:

- guardar confianza.
- guardar evidencias.
- guardar decision humana.

Metodos conceptuales:

- `is_above_threshold()`.
- `requires_manual_review()`.
- `accept(user_id)`.
- `reject(user_id, reason)`.

### AuditEvent

Evento auditable.

Responsabilidad:

- registrar accion, actor, entidad, estado anterior, estado nuevo y motivo.

Metodos conceptuales:

- `from_state_change()`.
- `from_decision()`.
- `from_exception()`.
- `from_security_event()`.

### ProcessEvent

Evento de proceso explotable analiticamente.

Responsabilidad:

- registrar que ocurrio en el flujo y permitir metricas.

Metodos conceptuales:

- `from_domain_event()`.
- `with_correlation_id(correlation_id)`.

En MVP puede convivir dentro de `audit_events` si no se separa fisicamente todavia.

### BuyerGroup

Grupo comprador o grupo responsable.

Responsabilidad:

- agrupar usuarios responsables de proveedores o movimientos.
- alimentar alertas y control de cierre.

Metodos conceptuales:

- `add_member(user_id)`.
- `remove_member(user_id)`.
- `deactivate()`.

La fuente puede ser ERP o configuracion interna.

### SupplierResponsibility

Relacion proveedor y grupo responsable.

Responsabilidad:

- determinar a quien alertar por movimientos abiertos, excepciones o cierre.

Metodos conceptuales:

- `is_active_on(date)`.
- `assign_group(group_id)`.
- `end_assignment(date)`.

### Alert

Aviso operativo.

Responsabilidad:

- notificar a usuario o grupo sobre una accion pendiente.

Metodos conceptuales:

- `acknowledge(user_id)`.
- `resolve(user_id, resolution)`.
- `escalate(reason)`.
- `is_overdue(reference_date)`.

### ClosingPeriod

Periodo de cierre operativo o financiero.

Responsabilidad:

- permitir control de fechas clave.
- asociar alertas a periodos.
- identificar pendientes antes de cierre.

Metodos conceptuales:

- `is_open()`.
- `is_closed()`.
- `is_near_deadline(reference_date)`.

## Servicios de dominio

### ProvisioningPolicy

Responsabilidad:

- decidir si un movimiento puede generar provision.
- decidir si requiere validacion.
- decidir si requiere mapeo proveedor.

Metodos conceptuales:

- `can_create_from(movement)`.
- `requires_administration_validation(request)`.
- `requires_supplier_mapping(request)`.

### ProvisionCompatibilityService

Responsabilidad:

- evaluar compatibilidad entre factura y provision.

Metodos conceptuales:

- `is_compatible(invoice, provision)`.
- `score_match(invoice, provision)`.
- `explain_match(invoice, provision)`.

### SupplierGovernanceService

Responsabilidad:

- decidir si el proveedor fiscal permite continuar el flujo.

Metodos conceptuales:

- `exists_for_legal_entity(supplier, legal_entity_id)`.
- `requires_onboarding(invoice)`.
- `can_continue_invoice_flow(invoice)`.

### AlertPolicy

Responsabilidad:

- decidir cuando generar alertas.

Metodos conceptuales:

- `should_alert_open_provision(provision, closing_period)`.
- `should_alert_missing_supplier(invoice)`.
- `should_alert_unresolved_exception(exception, closing_period)`.

## Casos de uso de application

Primer incremento:

- `CreateInternalOrder`.
- `GenerateProvisionFromMovement`.
- `RegisterInvoice`.
- `FindCompatibleProvisions`.
- `ApproveProvisionConsumption`.
- `RegisterAuditEvent`.

MVP ampliado:

- `CreateLateProvision`.
- `CreateSupplierOnboardingRequest`.
- `ConfirmSupplierCreatedInErp`.
- `ValidateSupplierMapping`.
- `GenerateClosingAlerts`.
- `ResolveAlert`.

## Reglas de diseno

- La API expone casos de uso, no tablas.
- El motor trabaja contra `ProvisionableMovement`.
- Cada origen implementa su forma de aportar datos.
- El dominio no llama a base de datos.
- El dominio no llama al ERP.
- El dominio no conoce FastAPI.
- La auditoria no es opcional.
- Las sugerencias de IA siempre requieren decision humana para convertirse en verdad contable.

## Alcance del primer desarrollo

Implementar primero:

- movimiento provisionable desde pedido interno.
- creacion de provision.
- registro de factura.
- busqueda de provisiones compatibles.
- consumo factura-provision.
- auditoria estructurada.

Preparar conceptualmente:

- proveedor fiscal inexistente.
- alta proveedor ERP simulada.
- matching y confianza.
- grupos responsables.
- alertas y control de cierre.
