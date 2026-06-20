# Contexto para agentes

## Objetivo

Este documento resume el estado de ProvCore para que un agente pueda incorporarse al proyecto sin reconstruir todo el contexto desde cero.

Debe leerse junto con `AGENTS.md`.

## Que es ProvCore

ProvCore es un motor comun de provisiones para conectar compromisos de gasto, facturas de proveedor y movimientos de tarjetas corporativas con trazabilidad contable completa.

La regla central del proyecto es:

```text
Ninguna factura debe contabilizarse definitivamente sin consumir una provision previa o una provision tardia auditada.
```

El sistema separa:

- usuario operativo.
- proveedor operativo.
- proveedor fiscal.
- Administracion.
- ERP.
- IA/OCR como herramienta de sugerencia.

La IA no es fuente de verdad contable. Administracion valida.

## Estado actual

El repositorio esta en fase de definicion funcional, decisiones de arquitectura y preparacion para prototipo.

No se ha iniciado todavia codigo de backend ni frontend.

Ya existen:

- especificacion funcional.
- arquitectura funcional.
- modelo de datos inicial.
- estados por entidad.
- casos de uso.
- diagramas Mermaid.
- roadmap MVP.
- backlog de issues.
- estructura de issues GitHub.
- decisiones 0001, 0002 y 0003.

## Decisiones tomadas

### Decision 0001 - Alcance del MVP

MVP objetivo:

- flujo principal.
- provision tardia auditada.
- mapeo proveedor operativo-fiscal basico.
- auditoria.
- analitica minima.

Primer incremento:

```text
Pedido interno -> Provision -> Factura -> Consumo -> Auditoria
```

Documento:

- `docs/decisiones/0001-alcance-mvp.md`

### Decision 0002 - Formato del prototipo

Stack aprobado:

```text
FastAPI + SQL Server + SQL Server Management Studio + frontend simple
```

Ejecucion:

- backend-first.
- alcance controlado.
- frontend simple despues de estabilizar flujo backend.

Documento:

- `docs/decisiones/0002-formato-prototipo.md`

### Decision 0003 - Arquitectura backend

Arquitectura aprobada:

- modular.
- orientada a clean architecture.
- dominio separado de FastAPI y SQL Server.
- modulo central `provisioning_engine`.
- implementacion pragmatica durante el MVP.
- evolucion a clean architecture mas estricta despues del MVP.

Documento:

- `docs/decisiones/0003-arquitectura-backend.md`

## Modulos iniciales

### provisioning_engine

Modulo central del sistema.

Responsabilidades:

- crear provisiones desde origenes.
- mantener reglas comunes de provision.
- consumir provisiones.
- permitir consumos parciales.
- permitir relacion N a N entre facturas y provisiones.
- calcular diferencias.
- preparar regularizaciones.
- emitir eventos o solicitudes de auditoria funcional.

No debe depender de:

- pedido interno.
- facturas.
- tarjetas.
- FastAPI.
- SQL Server.

### internal_orders

Origen operativo del flujo principal.

Responsabilidades:

- capturar compromiso de gasto.
- informar datos operativos.
- solicitar generacion de provision al motor.

No debe implementar reglas propias de provision.

### invoices

Modulo de facturas.

Responsabilidades:

- registrar factura.
- buscar provisiones compatibles.
- solicitar consumo al motor.
- activar provision tardia cuando no exista provision compatible.

No debe duplicar reglas del motor comun.

### audit

Modulo transversal.

Responsabilidades:

- registrar decisiones.
- registrar cambios de estado.
- registrar motivos.
- permitir reconstruir el ciclo de una provision.

La auditoria no debe ser un añadido final.

## Issues principales

Issues cerradas:

- #2 Definir alcance exacto del MVP.
- #9 Definir prototipo navegable.
- #10 Definir arquitectura tecnica minima del backend.

Issues abiertas relevantes:

- #1 Revisar modelo de datos inicial.
- #3 Crear pedido interno de gasto.
- #4 Generar provision desde pedido interno.
- #5 Buscar provisiones compatibles desde factura.
- #6 Aprobar consumo factura-provision.
- #7 Crear provision tardia auditada.
- #8 Auditar cambios de estado y decisiones.

## Siguiente decision pendiente

La siguiente decision debe tratar persistencia y migraciones con SQL Server.

Temas a decidir:

- SQLAlchemy o pyodbc directo.
- Alembic o scripts SQL manuales.
- patron Unit of Work.
- manejo de transacciones.
- organizacion de modelos ORM.
- separacion entre entidades de dominio y modelos persistidos.
- validacion manual con SQL Server Management Studio.

No implementar codigo antes de cerrar esta decision.

## Documentos clave por tarea

Para entender vision:

- `README.md`
- `docs/contexto_funcional.md`

Para entender arquitectura:

- `docs/arquitectura_funcional.md`
- `docs/decisiones/0003-arquitectura-backend.md`

Para entender dominio:

- `docs/modelo_datos_inicial.md`
- `docs/estados_entidades.md`
- `docs/casos_uso_detallados.md`

Para entender flujo:

- `docs/diagramas_flujo.md`

Para planificar trabajo:

- `docs/roadmap_mvp.md`
- `docs/github_issues.md`
- `docs/issues_backlog.md`

## Reglas para agentes

- No asumir que el primer modulo implementado define el dominio.
- No convertir pedido interno en centro del sistema.
- No poner reglas de provision dentro de invoices.
- No poner reglas de provision dentro de internal_orders.
- No usar SQL Server desde capas de dominio o application.
- No usar FastAPI fuera de interface.
- No introducir IA real en el MVP inicial.
- No crear frontend complejo antes de cerrar backend.
- No crear codigo sin issue o decision asociada.

## Criterio de avance

El proyecto avanza correctamente si cada paso cumple:

- decision documentada cuando afecte arquitectura.
- issue vinculada cuando afecte implementacion.
- dominio protegido de frameworks.
- persistencia aislada.
- trazabilidad funcional mantenida.
- documentacion actualizada.
