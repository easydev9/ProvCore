# Modelo de usuarios, roles y autorizacion

## Objetivo

Definir los perfiles de usuario iniciales de ProvCore y como se relacionan con roles, permisos, alcance, auditoria y seguridad.

Este documento prepara el diseno de API y backend. No implementa aun autenticacion real.

## Principio

```text
Un usuario no queda autorizado solo por existir.
```

Toda accion debe evaluarse con:

- usuario autenticado.
- rol asignado.
- permiso concreto.
- tenant.
- legal entity cuando aplique.
- estado de la entidad.
- alcance funcional.

## Diferencia entre usuario, rol, permiso y alcance

### Usuario

Persona o servicio autenticado en el sistema.

Ejemplos:

- una persona que crea pedidos.
- una persona que valida consumos.
- un servicio que sincroniza proveedores.

### Rol

Conjunto funcional de responsabilidades.

Ejemplo:

```text
Usuario financiero autorizado
```

### Permiso

Capacidad concreta de ejecutar una accion.

Ejemplo:

```text
approve_provision_consumption
```

### Alcance

Limite dentro del que el permiso es valido.

Ejemplo:

```text
tenant = grupo_energia
legal_entity = sociedad_es
buyer_group = compras_it
```

## Perfiles iniciales

### Usuario operativo

Responsabilidad:

- crear pedidos internos.
- informar proveedor conocido.
- adjuntar soporte.
- clasificar movimientos.
- validar que una factura corresponde al servicio.
- resolver alertas operativas asignadas.

No puede:

- validar proveedor fiscal.
- aprobar consumo contable.
- crear provision tardia.
- aprobar regularizaciones.
- modificar integraciones ERP.

Permisos posibles:

- create_internal_order.
- update_own_internal_order.
- validate_service_delivery.
- upload_support_document.
- classify_card_movement.
- acknowledge_alert.
- resolve_operational_alert.
- view_own_operational_analytics.

### Usuario financiero autorizado

Responsabilidad:

- validar proveedor fiscal.
- validar mapeo proveedor operativo-fiscal.
- aprobar consumo factura-provision.
- crear provision tardia.
- aprobar regularizaciones.
- revisar deducibilidad.
- desbloquear factura por motivo financiero.
- consultar analitica financiera dentro de su alcance.

Permisos posibles:

- validate_fiscal_supplier.
- approve_supplier_mapping.
- reject_supplier_mapping.
- approve_provision_consumption.
- create_late_provision.
- approve_regularization.
- unblock_invoice_financially.
- view_financial_analytics.
- view_audit_log.

### Supervisor financiero

Responsabilidad:

- revisar cierre.
- resolver excepciones criticas.
- aprobar decisiones de mayor riesgo.
- consultar informacion agregada.
- escalar incidencias.

Permisos posibles:

- approve_high_risk_exception.
- reopen_closing_period.
- view_cross_entity_financial_analytics.
- resolve_escalated_alert.
- review_late_provision_report.

### Administrador de tenant

Responsabilidad:

- gestionar usuarios del tenant.
- asignar roles.
- asignar legal entities.
- gestionar buyer groups.
- mantener configuracion funcional.

Permisos posibles:

- manage_tenant_users.
- assign_roles.
- assign_legal_entities.
- manage_buyer_groups.
- manage_supplier_responsibility.

No implica permisos contables por defecto.

### Administrador tecnico

Responsabilidad:

- configurar integraciones ERP.
- configurar pools de infraestructura.
- revisar health checks.
- mantener parametros tecnicos.
- gestionar credenciales tecnicas.

Permisos posibles:

- manage_erp_connections.
- manage_routing_policies.
- view_health_checks.
- manage_technical_credentials.
- view_integration_events.

No implica permisos contables por defecto.

### Servicio de integracion

Responsabilidad:

- ejecutar OCR.
- sincronizar maestros ERP.
- enviar solicitudes a ERP.
- ejecutar jobs programados.
- registrar eventos de integracion.

Permisos posibles:

- read_invoice_input.
- suggest_invoice_data.
- sync_erp_suppliers.
- submit_supplier_onboarding_to_erp.
- register_integration_event.

No puede aprobar decisiones humanas.

### Auditor

Responsabilidad:

- consultar auditoria.
- revisar trazabilidad.
- exportar evidencias.
- verificar decisiones.

Permisos posibles:

- view_audit_log.
- view_process_events.
- export_audit_evidence.

No modifica el flujo.

## Matriz inicial de responsabilidades

| Accion | Usuario operativo | Usuario financiero autorizado | Supervisor financiero | Administrador de tenant | Administrador tecnico | Servicio integracion | Auditor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Crear pedido interno | Si | No | No | No | No | No | No |
| Validar servicio recibido | Si | No | No | No | No | No | No |
| Validar proveedor fiscal | No | Si | Si | No | No | No | No |
| Aprobar consumo provision | No | Si | Si | No | No | No | No |
| Crear provision tardia | No | Si | Si | No | No | No | No |
| Aprobar regularizacion | No | Si | Si | No | No | No | No |
| Gestionar buyer groups | No | No | No | Si | No | No | No |
| Gestionar usuarios | No | No | No | Si | No | No | No |
| Configurar ERP | No | No | No | No | Si | No | No |
| Ejecutar sincronizacion ERP | No | No | No | No | No | Si | No |
| Consultar auditoria | No | Si | Si | No | No | No | Si |

## Alcance por rol

Un mismo rol puede tener alcances distintos.

Ejemplos:

```text
Usuario financiero autorizado
tenant: grupo_a
legal_entity: sociedad_es
```

```text
Supervisor financiero
tenant: grupo_a
legal_entity: sociedad_es, sociedad_fr
```

```text
Usuario operativo
tenant: grupo_a
buyer_group: compras_it
proveedor: proveedor_x
```

## Reglas de autorizacion por caso

### Crear pedido interno

Requiere:

- usuario operativo.
- tenant valido.
- legal entity permitida.
- area o buyer group permitido.

### Validar proveedor fiscal

Requiere:

- usuario financiero autorizado.
- permiso `validate_fiscal_supplier`.
- legal entity de la factura.
- auditoria obligatoria.

### Aprobar consumo factura-provision

Requiere:

- usuario financiero autorizado.
- permiso `approve_provision_consumption`.
- acceso a la legal entity de factura y provision.
- factura en estado permitido.
- provision consumible.
- auditoria obligatoria.

### Crear provision tardia

Requiere:

- usuario financiero autorizado.
- permiso `create_late_provision`.
- motivo obligatorio.
- factura origen.
- legal entity permitida.
- auditoria obligatoria.

### Gestionar routing

Requiere:

- administrador tecnico.
- permiso `manage_routing_policies`.
- tenant o entorno tecnico permitido.
- auditoria tecnica.

## Auditoria de autorizacion

Las decisiones relevantes deben registrar:

- user_id.
- rol usado.
- permiso usado.
- tenant_id.
- legal_entity_id.
- entidad afectada.
- estado anterior.
- estado posterior.
- motivo.
- fecha_hora.
- correlation_id.

## Criterio de uso de area financiera

Usar `usuario financiero autorizado` cuando se hable de:

- validar proveedor fiscal.
- validar mapeo fiscal.
- aprobar consumo.
- crear provision tardia.
- revisar impuestos.
- aprobar regularizaciones.
- desbloquear factura por criterio financiero.

Usar `area financiera` cuando se hable de:

- conversaciones de discovery.
- gobierno funcional del proceso.
- validacion organizativa fuera del sistema.
- contexto de negocio no ligado a permisos concretos.

## Alcance MVP

El MVP debe simular:

- usuario operativo.
- usuario financiero autorizado.
- administrador de tenant.
- servicio de integracion.

El primer backend puede empezar con usuarios semilla y permisos simples, pero no debe mezclar roles en la logica de negocio.
