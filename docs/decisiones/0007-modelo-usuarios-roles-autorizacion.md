# Decision 0007 - Modelo de usuarios, roles y autorizacion

## Estado

Aceptada.

## Contexto

ProvCore necesita distinguir usuarios, roles, permisos y alcance antes de disenar contratos API o implementar seguridad.

El gobierno fiscal y contable debe representarse con un modelo de usuarios, roles, permisos y alcance. Desde esta decision, el termino profesional para el area organizativa sera `area financiera`. Como modelo de producto SaaS, el sistema no debe depender de un departamento concreto como rol tecnico. Debe trabajar con usuarios autenticados, roles asignados y permisos acotados por tenant, legal entity y ambito operativo.

## Problema

Usar `usuario` de forma generica es insuficiente.

Riesgos:

- cualquier usuario podria parecer autorizado para validar verdad contable.
- no queda claro quien puede desbloquear facturas.
- no queda claro quien puede aprobar consumos o regularizaciones.
- no se distingue configuracion tecnica de decision financiera.
- no se prepara el modelo para RBAC, permisos ni alcance por sociedad.

Usar `area financiera` como actor tecnico tambien es limitado porque representa un area funcional, no un perfil de seguridad.

## Decision

ProvCore usara un modelo basado en:

```text
usuario
-> roles
-> permisos
-> alcance
```

El rol que representa acciones de validacion dentro del sistema sera:

```text
Usuario financiero autorizado
```

La expresion `area financiera` se usara cuando el texto hable del area funcional o de validacion con negocio, no como actor tecnico de permisos.

## Perfiles iniciales

### Usuario operativo

Usuario que informa compromisos de gasto, pedidos, proveedores conocidos, adjuntos y validacion funcional del servicio.

No debe conocer ni modificar datos fiscales o contables sensibles.

### Usuario financiero autorizado

Usuario con permisos para validar proveedor fiscal, consumo de provision, deducibilidad, impuestos, regularizaciones, provision tardia y desbloqueos contables.

Es el rol que convierte sugerencias en decisiones contables validas dentro de su alcance.

### Supervisor financiero

Usuario con permisos ampliados para revisar cierres, consultar analitica agregada, resolver excepciones criticas y aprobar operaciones de mayor riesgo dentro de su alcance.

### Administrador de tenant

Usuario que gestiona usuarios, roles, legal entities, buyer groups y configuracion funcional del tenant.

No implica capacidad automatica para aprobar decisiones contables.

### Administrador tecnico

Usuario que gestiona configuracion tecnica, integraciones ERP, pools, routing, health checks y credenciales tecnicas.

No debe tomar decisiones contables por tener permisos tecnicos.

### Servicio de integracion

Actor no humano usado por OCR, ERP adapters, jobs programados, sincronizaciones o procesos batch.

Debe tener permisos minimos, trazables y limitados a su funcion.

### Auditor

Usuario con acceso de consulta a auditoria, eventos, decisiones y trazabilidad dentro de su alcance.

No modifica decisiones funcionales ni contables.

## Modelo de autorizacion

ProvCore combinara:

- RBAC para roles y permisos.
- Alcance por tenant, legal entity, buyer group, proveedor, area o pais.
- Reglas de estado para impedir acciones fuera del ciclo permitido.

Ejemplo:

```text
Puede aprobar consumo
si tiene permiso approve_provision_consumption
y pertenece al tenant de la factura
y tiene acceso a la legal entity
y la factura esta en estado permitido
y la decision queda auditada
```

## Permisos iniciales

Permisos funcionales:

- create_internal_order.
- validate_service_delivery.
- validate_fiscal_supplier.
- approve_supplier_mapping.
- reject_supplier_mapping.
- approve_provision_consumption.
- create_late_provision.
- approve_regularization.
- resolve_closing_alert.
- view_operational_analytics.
- view_financial_analytics.
- manage_buyer_groups.
- manage_tenant_users.
- manage_erp_connections.
- manage_routing_policies.
- view_audit_log.

## Alcance

Todo permiso debe evaluarse dentro de un alcance.

Alcances posibles:

- tenant.
- legal entity.
- pais.
- area.
- buyer group.
- proveedor.
- periodo.

Regla:

```text
Un permiso sin alcance valido no autoriza la operacion.
```

## Reglas de seguridad

- Todo usuario autenticado opera dentro de tenant y alcance asignado.
- Toda operacion fiscal o contable requiere legal entity.
- El usuario operativo no puede validar proveedor fiscal ni consumo contable.
- El usuario financiero autorizado no obtiene permisos tecnicos por defecto.
- El administrador tecnico no obtiene permisos contables por defecto.
- Los servicios de integracion tienen permisos minimos y auditables.
- Toda decision contable debe registrar usuario, rol usado, permiso y alcance.

## Implicaciones para documentacion

Cuando una accion requiera permisos dentro del sistema, se usara `usuario financiero autorizado`.

Cuando el texto represente el area funcional, se usara `area financiera`.

Estados derivados:

- `PendienteValidacionFinanciera`.
- `ValidadoFinanciero`.

## MVP

El MVP puede empezar con roles simulados.

Minimo necesario:

- usuario operativo.
- usuario financiero autorizado.
- administrador de tenant.
- servicio de integracion.
- auditoria con usuario, rol y accion.

No entra inicialmente:

- proveedor externo de identidad.
- SSO real.
- MFA.
- politicas complejas ABAC.
- segregacion de funciones avanzada.

## Consecuencias

### Positivas

- Evita ambiguedad entre usuario generico y autoridad contable.
- Prepara seguridad, autorizacion y auditoria.
- Encaja con SaaS, tenant y legal entity.
- Permite separar decisiones financieras y gestión técnica.

### Costes

- Exige modelar permisos desde el inicio.
- Aumenta campos de auditoria.
- Obliga a definir alcance en casos de uso y API.
- Los tests futuros deberan cubrir autorizacion y denegacion.

## Reglas derivadas

- No usar `usuario` como sinonimo de autoridad contable.
- No usar departamentos como roles tecnicos.
- Usar `usuario financiero autorizado` para decisiones contables.
- Separar rol, permiso y alcance.
- Auditar rol y permiso usado en decisiones relevantes.
