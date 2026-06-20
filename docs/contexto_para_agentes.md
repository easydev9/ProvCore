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
- usuario financiero autorizado.
- ERP.
- IA/OCR como herramienta de sugerencia.

La IA no es fuente de verdad contable. El usuario financiero autorizado valida.

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
- decisiones 0001, 0002, 0003, 0004, 0005, 0006 y 0007.
- vision estrategica de producto.
- modelo de dominio MVP.
- definition of done.
- glosario.

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

### Decision 0004 - Persistencia y migraciones

Persistencia aprobada:

```text
SQLAlchemy ORM + Alembic + pyodbc + Unit of Work
```

Regla no negociable:

- SQLAlchemy y pyodbc solo viven en infrastructure.
- Domain no conoce ORM.
- Application no conoce SQLAlchemy.
- Unit of Work controla commit y rollback.
- Alembic gobierna cambios de esquema.
- SQL Server Management Studio valida e inspecciona, pero no sustituye migraciones.

Documento:

- `docs/decisiones/0004-persistencia-migraciones.md`

### Decision 0005 - Modelo SaaS tenant-aware

ProvCore se disena como SaaS tenant-aware.

Conceptos:

- `tenant`: cliente o grupo empresarial.
- `legal_entity`: sociedad dentro del tenant.
- el tenant es frontera de seguridad.
- las entidades operativas principales deben contemplar tenant.
- las entidades fiscales y contables deben contemplar legal entity.
- el alta de proveedor fiscal depende de tenant, legal entity y ERP.

Documento:

- `docs/decisiones/0005-modelo-saas-tenant-aware.md`

### Decision 0006 - Routing funcional multi-sociedad

ProvCore separa routing funcional y balanceo tecnico.

Reglas:

- primero se resuelve tenant, legal entity, permisos, residencia del dato e integracion asociada.
- despues se selecciona el pool de infraestructura autorizado.
- el balanceo tecnico opera solo dentro del pool autorizado.
- las reglas de routing viven fuera del dominio.

Documento:

- `docs/decisiones/0006-routing-funcional-multisociedad.md`
- `docs/arquitectura_routing_multisociedad.md`

### Decision 0007 - Modelo de usuarios, roles y autorizacion

ProvCore separa usuario, rol, permiso y alcance.

Reglas:

- `usuario financiero autorizado` sustituye a `Administracion` cuando el texto hable de acciones de validacion dentro del sistema.
- `Administracion` solo debe mantenerse cuando represente area funcional o contexto de discovery.
- todo permiso se evalua por tenant y alcance.
- toda operacion fiscal o contable requiere legal entity.
- servicios de integracion no pueden aprobar decisiones humanas.

Documentos:

- `docs/decisiones/0007-modelo-usuarios-roles-autorizacion.md`
- `docs/modelo_usuarios_roles_autorizacion.md`

## Modulos iniciales

### provisioning_engine

Modulo central del sistema.

Responsabilidades:

- identificar movimientos provisionables.
- normalizar cada origen antes de aplicar reglas comunes.
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
- #11 Definir persistencia y migraciones.
- #12 Definir vision estrategica SaaS y modelo de dominio MVP.
- #13 Definir routing funcional multi-sociedad.
- #14 Definir modelo de usuarios, roles y autorizacion.

Issues abiertas relevantes:

- #1 Revisar modelo de datos inicial.
- #3 Crear pedido interno de gasto.
- #4 Generar provision desde pedido interno.
- #5 Buscar provisiones compatibles desde factura.
- #6 Aprobar consumo factura-provision.
- #7 Crear provision tardia auditada.
- #8 Auditar cambios de estado y decisiones.

## Siguiente decision pendiente

La siguiente decision debe tratar contratos de API y formato de errores.

Temas a decidir:

- prefijo de API.
- versionado.
- formato de respuesta.
- formato de error.
- codigos HTTP.
- traduccion de errores de dominio a HTTP.

No implementar endpoints antes de cerrar esta decision.

## Documentos clave por tarea

Para entender vision:

- `README.md`
- `docs/contexto_funcional.md`

Para entender arquitectura:

- `docs/arquitectura_funcional.md`
- `docs/decisiones/0003-arquitectura-backend.md`
- `docs/decisiones/0004-persistencia-migraciones.md`
- `docs/decisiones/0005-modelo-saas-tenant-aware.md`
- `docs/decisiones/0006-routing-funcional-multisociedad.md`
- `docs/decisiones/0007-modelo-usuarios-roles-autorizacion.md`
- `docs/arquitectura_routing_multisociedad.md`
- `docs/modelo_usuarios_roles_autorizacion.md`

Para entender dominio:

- `docs/glosario.md`
- `docs/modelo_dominio_mvp.md`
- `docs/modelo_datos_inicial.md`
- `docs/estados_entidades.md`
- `docs/casos_uso_detallados.md`

Para entender vision estrategica:

- `docs/vision_estrategica_producto.md`

Para entender flujo:

- `docs/diagramas_flujo.md`

Para planificar trabajo:

- `docs/definition_of_done.md`
- `docs/roadmap_mvp.md`
- `docs/github_issues.md`
- `docs/issues_backlog.md`

## Reglas para agentes

- No asumir que el primer modulo implementado define el dominio.
- No convertir pedido interno en centro del sistema.
- No modelar el motor como CRUD de pedidos o facturas.
- Identificar siempre el movimiento provisionable y su origen.
- Considerar tenant y legal entity en datos operativos, fiscales y analiticos.
- Bloquear factura cuando el proveedor fiscal no exista para la legal entity.
- Registrar evento o auditoria para decisiones, bloqueos, alertas y excepciones.
- Separar routing funcional y balanceo tecnico.
- No poner reglas de infraestructura en domain.
- Separar usuario, rol, permiso y alcance.
- No usar usuario generico como autoridad contable.
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
