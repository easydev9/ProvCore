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
- Auditar decisiones de Administracion.
- Reportar excepciones.
- Regularizar diferencias.

### M3 - Gobierno de proveedores

Objetivo:

Separar proveedor operativo y proveedor fiscal con validacion de Administracion.

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

## Uso recomendado

1. Crear primero las labels.
2. Crear milestones `M0` a `M5`.
3. Abrir las issues iniciales sugeridas.
4. Marcar como `mvp` solo las issues que entren en la primera version.
5. Mantener el backlog documental como fuente funcional y GitHub Issues como gestion del trabajo.
