# Estructura de issues GitHub

## Objetivo

Definir una estructura de labels, epicas e issues iniciales para gestionar ProvCore en GitHub sin perder el hilo funcional del proyecto.

El backlog detallado vive en [Backlog de issues inicial](issues_backlog.md). Este documento traduce ese contenido a una organizacion practica para GitHub.

## Labels recomendadas

### Tipo

- `feature`: nueva capacidad funcional.
- `functional-analysis`: decision o refinamiento funcional.
- `documentation`: mejora documental.
- `bug`: inconsistencia o error.
- `prototype`: trabajo orientado al prototipo.

### Prioridad

- `P0`: imprescindible para validar el flujo central.
- `P1`: necesario para MVP.
- `P2`: ampliacion posterior.

### Modulo

- `module:provisions`.
- `module:internal-orders`.
- `module:suppliers`.
- `module:invoices`.
- `module:cards`.
- `module:audit`.
- `module:analytics`.
- `module:erp`.
- `module:api`.
- `module:tenants`.
- `module:alerts`.
- `module:closing`.
- `module:infrastructure`.
- `module:security`.

### Estado funcional

- `needs-decision`: requiere decidir criterio.
- `ready`: listo para trabajar.
- `blocked`: bloqueado por decision o dependencia.
- `mvp`: incluido en el MVP recomendado.

## Milestones recomendados

### M0 - Base funcional

Objetivo:

Consolidar documentacion, arquitectura, estados y backlog.

Issues candidatas:

- Revisar modelo de datos inicial.
- Revisar estados por entidad.
- Validar casos de uso principales.
- Revisar diagramas Mermaid.
- Priorizar backlog P0.
- Definir vision estrategica SaaS y modelo de dominio MVP.
- Validar tenant, legal entity y movimiento provisionable como base.
- Definir routing funcional multi-sociedad.
- Definir modelo de usuarios, roles y autorizacion.
- Definir contratos API MVP.

### M1 - Flujo principal

Objetivo:

Construir o especificar el flujo de pedido interno, provision, factura y consumo.

Issues candidatas:

- Crear pedido interno de gasto.
- Enviar pedido y generar provision.
- Crear entidad provision.
- Buscar provisiones abiertas compatibles.
- Aprobar relacion factura-provision.
- Auditar cambios de estado.

### M2 - Excepciones auditadas

Objetivo:

Cubrir factura sin provision previa y regularizaciones basicas.

Issues candidatas:

- Crear provision tardia.
- Auditar decisiones financieras autorizadas.
- Reportar excepciones.
- Regularizar diferencias.

### M3 - Gobierno de proveedores

Objetivo:

Separar proveedor operativo y proveedor fiscal con validacion de usuario financiero autorizado.

Issues candidatas:

- Registrar proveedor operativo.
- Sugerir proveedor fiscal.
- Validar mapeo proveedor.
- Rechazar o corregir mapeo.

### M4 - Analitica minima

Objetivo:

Mostrar seguimiento de provisionado, consumido, pendiente y excepciones.

Issues candidatas:

- Vista general por responsable.
- Vista detallada por provision.
- Reporte de provisiones tardias.

### M5 - Tarjetas corporativas

Objetivo:

Extender el motor comun a movimientos de tarjeta.

Issues candidatas:

- Importar movimiento de tarjeta.
- Asociar factura a movimiento de tarjeta.
- Marcar movimiento sin factura.
- Asociar factura agrupada a varios movimientos.

## Issues iniciales sugeridas

### 1. Revisar modelo de datos inicial

Labels:

```text
functional-analysis, documentation, P0, module:provisions, ready
```

Objetivo:

Validar que las entidades principales cubren pedido interno, provision, factura, consumo, mapeo, tarjeta, regularizacion y auditoria.

### 2. Definir alcance exacto del MVP

Labels:

```text
functional-analysis, P0, mvp, needs-decision
```

Objetivo:

Confirmar si el MVP incluye solo flujo principal y provision tardia, o tambien mapeo proveedor operativo-fiscal y analitica minima.

### 3. Crear pedido interno de gasto

Labels:

```text
feature, P0, module:internal-orders, mvp, ready
```

Objetivo:

Permitir que el responsable notifique un compromiso sin informar datos fiscales.

### 4. Generar provision desde pedido interno

Labels:

```text
feature, P0, module:provisions, mvp, ready
```

Objetivo:

Crear `id_provision` y provision asociada al pedido interno.

### 5. Buscar provisiones compatibles desde factura

Labels:

```text
feature, P0, module:invoices, module:provisions, mvp, ready
```

Objetivo:

Sugerir provisiones abiertas compatibles al registrar una factura.

### 6. Aprobar consumo factura-provision

Labels:

```text
feature, P0, module:invoices, module:provisions, mvp, ready
```

Objetivo:

Permitir consumo total o parcial y actualizar importes de provision.

### 7. Crear provision tardia auditada

Labels:

```text
feature, P0, module:invoices, module:audit, mvp, ready
```

Objetivo:

Resolver facturas sin provision previa mediante una excepcion obligatoriamente justificada y auditable.

### 8. Auditar cambios de estado y decisiones

Labels:

```text
feature, P0, module:audit, mvp, ready
```

Objetivo:

Registrar usuario, fecha, accion, estado anterior, estado posterior y motivo cuando aplique.

### 9. Definir prototipo navegable

Labels:

```text
functional-analysis, prototype, P0, mvp, needs-decision
```

Objetivo:

Elegir si el primer prototipo sera maqueta navegable, app web con datos en memoria o API con base de datos ligera.

### 10. Definir arquitectura tecnica minima del backend

Labels:

```text
functional-analysis, prototype, P0, mvp, needs-decision
```

Objetivo:

Decidir arquitectura modular, capas, modulos iniciales y reglas de dependencia del backend.

### 11. Definir persistencia y migraciones

Labels:

```text
functional-analysis, prototype, P0, mvp, needs-decision
```

Objetivo:

Decidir ORM, migraciones, driver SQL Server y patron de transaccion.

### 12. Definir vision estrategica SaaS y modelo de dominio MVP

Labels:

```text
functional-analysis, documentation, P0, mvp, module:tenants, module:analytics, ready
```

Objetivo:

Documentar vision SaaS tenant-aware, movimiento provisionable, modelo de dominio, eventos, alertas, buyer groups y alta de proveedor fiscal.

### 13. Definir routing funcional multi-sociedad

Labels:

```text
functional-analysis, documentation, P1, module:tenants, module:infrastructure, ready
```

Objetivo:

Separar routing funcional, pool autorizado y balanceo tecnico para escenarios con multiples sociedades e infraestructuras.

### 14. Definir modelo de usuarios, roles y autorizacion

Labels:

```text
functional-analysis, documentation, P0, mvp, module:security, module:tenants, ready
```

Objetivo:

Definir usuarios, roles, permisos, alcance y criterio de uso de usuario financiero autorizado para decisiones contables dentro del sistema.

### 15. Definir contratos API MVP

Labels:

```text
functional-analysis, documentation, P0, mvp, module:api, ready
```

Objetivo:

Definir endpoints, actores, permisos, formato de respuesta, formato de error, eventos y reglas de seguridad del MVP.

### 16. Modelar alta de proveedor fiscal para ERP simulado

Labels:

```text
feature, P1, module:suppliers, module:erp, mvp, ready
```

Objetivo:

Preparar el flujo donde una factura queda bloqueada hasta confirmar proveedor fiscal para la legal entity.

### 17. Generar alertas de cierre por grupo responsable

Labels:

```text
feature, P1, module:alerts, module:closing, module:analytics, ready
```

Objetivo:

Crear alertas para grupos compradores o responsables cuando existan pendientes antes del cierre.

## Uso recomendado

1. Crear primero las labels.
2. Crear milestones `M0` a `M5`.
3. Abrir las issues iniciales sugeridas.
4. Marcar como `mvp` solo las issues que entren en la primera version.
5. Mantener el backlog documental como fuente funcional y GitHub Issues como gestion del trabajo.
